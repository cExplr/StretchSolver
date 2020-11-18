from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QWidget, QGraphicsItem, QGraphicsLineItem, QPushButton
import sys
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QPolygon
from PyQt5.QtCore import Qt, QPointF, QPoint
import time
import math
import random


class Constants:
    gridPixHeight = 18
    gridPixWidth = 18


class Point(QPoint):
    def __init__(self, x, y):
        super().__init__(x, y)

    def plotPoint(self, scene,  pen):
        pointRadius = min(Constants.gridPixHeight, Constants.gridPixWidth)*0.3
        scene.addEllipse(self.x() * Constants.gridPixWidth - (pointRadius/2), self.y()*Constants.gridPixHeight - (pointRadius/2), pointRadius,
                         pointRadius, pen)


class Polygon(QPolygon):
    def __init__(self):
        pass


class Line(QGraphicsLineItem):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def getP1(self):
        return self.p1

    def getP2(self):
        return self.p2

    def setP1(self, p1):
        self.p1 = p1

    def setP2(self, p2):
        self.p2 = p2

    def getDistance(self):
        result = math.sqrt(abs(math.pow((self.p1.x() - self.p2.x()), 2) +
                               pow((self.p1.y() - self.p2.y()), 2)))
        # print("Distance between " + str(self.p1) +
        #      " and " + str(self.p2) + " is " + str(result))
        return result

    def drawStraightLine(self, scene, pen):
        lineItem = scene.addLine(self.getP1().x()*Constants.gridPixWidth, self.getP1().y() * Constants.gridPixHeight,
                                 self.getP2().x()*Constants.gridPixWidth, self.getP2().y()*Constants.gridPixHeight, pen)
        return lineItem


class FlapCircle:
    def __init__(self, radius, centerPoint):
        self.radius = radius
        self.centerPoint = centerPoint

    def getCenterPoint(self):
        return self.centerPoint

    def setCenterPoint(self, centerPoint):
        self.centerPoint = centerPoint

    def getRadius(self):
        return self.radius

    def setRadius(self, radius):
        self.radius = radius

    def drawFlap(self, scene, pen):
        """ reimplement once the core is being settled"""

        self.radius = math.ceil(self.radius)
        diameter = self.radius*2
        print("Cricle Center : (x ,y) = (" + str(self.centerPoint.x()
                                                 ) + "," + str(self.centerPoint.y()) + ")")
        print("Radius : " + str(self.radius))
        circle = scene.addEllipse(
            (self.centerPoint.x()-self.radius)*Constants.gridPixWidth, (self.centerPoint.y() - self.radius)*Constants.gridPixHeight, diameter * Constants.gridPixWidth, diameter * Constants.gridPixHeight, pen)

        return circle


class Rect:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getArea(self):
        return self.height * self.width


class OverlappingRectangle(Rect):
    def __init__(self, w, h):
        super().__init__(w, h)

    def isEven(self):
        return (self.getWidth()*self.getHeight()) % 2 == 0


class MarginRectangle(Rect):
    def __init__(self, w, h):
        super().__init__(w, h)


class SCR(Rect):
    def __init__(self, w, h):
        super().__init__(w, h)


class EmanatingLine(Line):
    # This draws the original emanating line from the center of the circle up to'
    # till the boundary of the box
    def __init__(self, circleList):
        super().__init__(Point(0, 0), Point(0, 0))


class Calculator:
    def __init__(self):
        pass

    def getDistance(self, p1, p2):
        result = math.sqrt(abs(math.pow((p1.x() - p2.x()), 2) +
                               pow((p1.y() - p2.y()), 2)))
        return result


class Stretch:
    def __init__(self):
        pass


class Gadget:
    def __init__(self, circle1, circle2):
        self.s1 = 0
        self.s2 = 0
        self.d = 0
        self.OR = None
        self.scr = None
        self.mRList = []
        self.topLeftFlap = None
        self.topRightFlap = None
        self.bottomLeftFlap = None
        self.bottomRightFlap = None
        self.notation = ""
        self.circle1 = circle1
        self.circle2 = circle2
        self.stretchPointsList = []  # contains list of points to join with lines

        self.s1 = self.calculateS1()
        self.s2 = self.calculateS2()
        self.d = self.calculateD()
        self.calculateMRList(self.calculateOR())

    def figureGadgetNotation(self):
        if self.circle1.getCenterPoint().x() < self.circle2.getCenterPoint().x() and self.circle1.getCenterPoint().y() < self.circle2.getCenterPoint().y():
            self.notation = "/"
            self.topLeftFlap = self.circle1
            self.bottomRightFlap = self.circle2
        elif self.circle1.getCenterPoint().x() < self.circle2.getCenterPoint().x() and self.circle1.getCenterPoint().y() > self.circle2.getCenterPoint().y():
            self.notation = "\\"
            self.bottomLeftFlap = self.circle1
            self.topRightFlap = self.circle2
        elif self.circle1.getCenterPoint().x() > self.circle2.getCenterPoint().x() and self.circle1.getCenterPoint().y() < self.circle2.getCenterPoint().y():
            self.notation = "\\"
            self.topRightFlap = self.circle1
            self.bottomLeftFlap = self.circle2
        elif self.circle1.getCenterPoint().x() > self.circle2.getCenterPoint().x() and self.circle1.getCenterPoint().y() > self.circle2.getCenterPoint().y():
            self.notation = "/"
            self.topLeftFlap = self.circle2
            self.bottomRightFlap = self.circle1

        else:
            print("ERRRRRRORRR Exiting")
            time.sleep(10)
            sys.exit(-1)

    def getCircle1(self):
        return self.circle1

    def getCircle2(self):
        return self.circle2

    def isForwardNotation(self, circle1, circle2):
        # (x,x)/(x,x)
        pass

    def calculateS1(self):
        self.s1 = abs(self.circle1.getCenterPoint().x() -
                      self.circle2.getCenterPoint().x())
        return self.s1

    def calculateS2(self):
        self.s2 = abs(self.circle1.getCenterPoint().y() -
                      self.circle2.getCenterPoint().y())

        return self.s2

    def calculateD(self):
        d = self.circle1.getRadius() + self.circle2.getRadius()
        return d

    """
    This should calculate and return a list of margin rectangle that are eligible for
    the creation of the gadgets
    """

    def calculateMRList(self, OR):
        # check if even or not
        # Deals with even first
        possibleFactors = []
        mRArea = 0

        for i in range(1, math.ceil(math.sqrt(OR.getArea()))):
            possibleFactors.append(i)

        if (OR.isEven()):
            mRArea = OR.getArea()/2
            for possibleFactor in possibleFactors:
                if (mRArea) % possibleFactor == 0:
                    temp = MarginRectangle(
                        mRArea/possibleFactor, possibleFactor)
                    if temp not in self.mRList:
                        self.mRList.append(temp)

        # Then deal with odd

        # Now that we know the list of possible MRs, we want to know if they are usable based on s1 and s2
        counter = 0
        while counter != len(self.mRList):
            if not(self.calculateSCRBasedOnMR(self.mRList[counter]).getWidth() <= self.calculateS1() and self.calculateSCRBasedOnMR(self.mRList[counter]).getHeight() <= self.calculateS2()):
                del self.mRList[counter]
            else:
                counter += 1

        length = len(self.mRList)
        for i in range(length):
            self.mRList.append(MarginRectangle(
                self.mRList[i].getHeight(), self.mRList[i].getWidth()))
        for i in self.mRList:
            print("[" + str(i.getWidth()) + "," + str(i.getHeight()) + "]")
        return self.mRList

    def calculateOR(self):

        d = self.circle1.getRadius() + self.circle2.getRadius()
        s1 = abs(self.circle1.getCenterPoint().x() -
                 self.circle2.getCenterPoint().x())
        s2 = abs(self.circle2.getCenterPoint().y() -
                 self.circle1.getCenterPoint().y())
        print("d , s1 , s2 , rad1 , rad2: ", d, s1, s2,
              self.circle1.getRadius(), self.circle2.getRadius())
        o1 = abs(d - s1)
        o2 = abs(d - s2)
        if o1 > 0 and o2 > 0:
            print(" -- OR : (" + str(o1) + "," + str(o2) + ")")
            self.OR = OverlappingRectangle(o1, o2)
            return self.OR
        else:
            return False

    def checkIfCirclesOverlapped(self):
        distBetCentres = Line(Point(self.circle1.getCenterPoint().x(), self.circle1.getCenterPoint().y()), Point(
            self.circle2.getCenterPoint().x(), self.circle2.getCenterPoint().y())).getDistance()

        return distBetCentres < (self.circle1.getRadius() + self.circle2.getRadius())

    def calculateSCRBasedOnMR(self, MR):
        SCR1 = MR.getWidth() + MR.getHeight() + self.OR.getHeight()
        SCR2 = MR.getWidth() + MR.getHeight() + self.OR.getWidth()
        self.SCR = SCR(SCR1, SCR2)
        print("SCR : " + str(self.SCR.getWidth()) + "," + str(self.SCR.getHeight()) +
              "}" + " --> MR(" + str(MR.getWidth()) + "," + str(MR.getHeight()) + ")")
        return self.SCR

    def plotGOPS(self, scene, MR, pen):
        # depending on the notation
        # point will always start from left side fir
        u, v = MR.getWidth(), MR.getHeight()
        pointList = []

        SCR = self.calculateSCRBasedOnMR(MR)
        self.figureGadgetNotation()
        scr1 = SCR.getWidth()
        scr2 = SCR.getHeight()
        tlCenter = self.topLeftFlap.getCenterPoint()
        brCenter = self.bottomRightFlap.getCenterPoint()

        pointList.append(Point(tlCenter.x(), tlCenter.y()))
        pointList.append(Point(tlCenter.x() + scr1 - u,  tlCenter.y() + v))
        pointList.append(Point(tlCenter.x() + scr1, tlCenter.y() + scr2))
        pointList.append(Point(tlCenter.x() + u, tlCenter.y() + scr2 - v))
        pointList.append(Point(tlCenter.x(), tlCenter.y()))
        print("pointList : ", pointList)
        for i in range(len(pointList)-1):
            print("ATTEMPTING TO DRAW")
            print(pointList[i].x(), pointList[i].y(
            ), pointList[i+1].x(), pointList[i+1].y(), pen)
            scene.addLine(pointList[i].x() * Constants.gridPixWidth, pointList[i].y() * Constants.gridPixHeight,
                          pointList[i+1].x() * Constants.gridPixWidth, pointList[i+1].y() * Constants.gridPixHeight, pen)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "GOPS/GPS Drawer"
        self.top = 0
        self.left = 0
        self.width = 1920
        self.height = 1080
        self.drawingView = ""
        self.initWindow()

    def initWindow(self):

        self.calculator = Calculator()
        # Setting windows text
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        # Deals with the objects to create drawings
        self.redPen = QPen(Qt.red)
        self.redPen.setWidth(2)
        self.blackPen = QPen(Qt.black)
        self.greenPen = QPen(Qt.green)
        self.blackPen.setWidth(1)  # For the grid outline
        self.greenPen.setWidth(1)
        self.whitePen = QPen(Qt.white)
        self.thickWhitePen = QPen(Qt.white)
        self.thickWhitePen.setWidth(2)

        self.grayBrush = QBrush(Qt.gray)
        self.redBrush = QBrush(Qt.red)
        self.blackBrush = QBrush(Qt.black)
        self.whiteBrush = QBrush(Qt.white)

        # The Drawing view
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 1920, 960)
        self.grayColor = QColor()
        self.grayColor.setRgb(0x252525)
        self.scene.setBackgroundBrush(self.grayColor)
        self.generateButtonClicked()

        # UI
        self.generateRandomButton = QPushButton(
            "Click to generate random pattern", self)
        self.generateRandomButton.resize(100, 400)
        self.generateRandomButton.move(0, 960)
        self.generateRandomButton.clicked.connect(self.generateButtonClicked)
        self.generateRandomButton.show()
        # Testing

    def generateButtonClicked(self):
        self.scene.clear()
        self.calculator = Calculator()
        rad1 = random.randint(1, 17)
        rad2 = random.randint(1, 17)
        self.drawGrid(0, 0)
        centerPoint1 = Point(0, 0)
        centerPoint2 = Point(0, 0)

        overlappingRectangle = None

        mainGadget = Gadget(FlapCircle(rad1, centerPoint1),
                            FlapCircle(rad2, centerPoint2))
        while True:
            # Here is to the generation of the random test cases that we wanna try
            """
            After deciding on two of the radiuses, let the 2 circles centers start from the same place
            for the generation, the radius of one of the circles would shift either up or down and check that the circles do not overlap
            if the circles do not overlap , that that there should still be an overlapping rectangle
            if there is no overlapping rectange while there is no overlapping of circles, then it fails the generation and it shoudl restart
            if there is overlapping rectangle with no overlapping circles, then it passes the test
            """

            if mainGadget.checkIfCirclesOverlapped() == True:

                if random.randint(0, random.randint(0, 100)) % 2 != 0:
                    # go down
                    mainGadget.getCircle2().getCenterPoint().setY(
                        mainGadget.getCircle2().getCenterPoint().y() + 1)
                else:
                    mainGadget.getCircle2().getCenterPoint().setX(
                        mainGadget.getCircle2().getCenterPoint().x() + 1)
            else:

                overlappingRectangle = mainGadget.calculateOR()
                if overlappingRectangle == False:
                    # restart again
                    mainGadget.getCircle2().getCenterPoint().setX(0)
                    mainGadget.getCircle2().getCenterPoint().setY(0)
                    rad1 = random.randint(1, 10)
                    rad2 = random.randint(1, 10)
                    mainGadget.getCircle2().setRadius(rad2)
                    mainGadget.getCircle1().setRadius(rad1)

                else:
                    break

            # self.drawGrid(x, y)

        self.drawGrid(max(centerPoint1.x(), centerPoint2.x()), max(
            centerPoint1.y(), centerPoint2.y()))
        centerPoint1.plotPoint(self.scene, self.greenPen)
        centerPoint2.plotPoint(self.scene, self.greenPen)
        mainGadget.calculateS1()
        mainGadget.calculateS2()
        mainGadget.calculateD()
        mainGadget.calculateMRList(mainGadget.calculateOR())
        for mr in mainGadget.mRList:
            mainGadget.calculateSCRBasedOnMR(mr)
        lengthToEmanate = 0
        if len(mainGadget.mRList) >= 1:
            mainGadget.plotGOPS(
                self.scene, mainGadget.mRList[0], self.greenPen)
            lengthToEmanate = mainGadget.calculateS1(
            ) - mainGadget.calculateSCRBasedOnMR(mainGadget.mRList[0]).getWidth()
        emanatingline = EmanatingLine(mainGadget.bottomRightFlap)
        emanatingline.drawStraightLine(self.scene, self.greenPen)
        flap1 = FlapCircle(rad1, centerPoint1)
        flap1.drawFlap(self.scene, self.greenPen)
        flap2 = FlapCircle(rad2, centerPoint2)
        flap2.drawFlap(self.scene, self.greenPen)
        """
        emanatingline1 = EmanatingLine(flap1)
        emanatingline2 = EmanatingLine(flap2)
        emanatingline1.drawStraightLine(self.scene, self.redPen)
        emanatingline2.drawStraightLine(self.scene, self.redPen)
        testline3 = Line(centerPoint1, centerPoint2)
        testline3.drawStraightLine(self.scene, self.redPen)
        testpoint = Point(1, 1)
        testpoint2 = Point(4, 4)
        self.plotPoint(testpoint)
        self.plotPoint(testpoint2)
        testline = Line(testpoint, testpoint2)
        testlineItem = self.drawStraightLine(testline, self.thickWhitePen)
        testlineItem.setFlag(QGraphicsItem.ItemIsMovable)
        """

        self.show()

    def drawGrid(self, nX, nY):
        # nX and nY refers to the number of grids there are in th x and y axis
        # Get the width of the current widnow we want to be able to scale effectively

        # hardcode for now

        self.totalPixHeight = Constants.gridPixHeight * nY
        self.totalPixWidth = Constants.gridPixWidth * nX

        for i in range(nY+1):
            self.scene.addLine(0, i*Constants.gridPixHeight,
                               self.totalPixWidth, i*Constants.gridPixHeight, self.whitePen)
        for i in range(nX+1):
            self.scene.addLine(i*Constants.gridPixWidth, 0,
                               i*Constants.gridPixWidth, self.totalPixHeight, self.whitePen)

        """
        self.line = self.scene.addLine(10, 10, 200, 200, self.blackPen)
        self.view.setMaximumWidth(600)
        self.view.setMaximumHeight(600)
        self.line.setFlag(QGraphicsItem.ItemIsMovable)
        """

    def reinit(self):
        self.initWindow()

    def getScene(self):
        return self.scene


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
