from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QWidget, QGraphicsItem, QGraphicsLineItem
import sys
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt
import time
import math
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    # def __str__(self):
    #    print("Point [" + str(self.getX()) + "," + str(self.getY())+"]")


class Line(QGraphicsLineItem):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def getP1(self):
        return self.p1

    def getP2(self):
        return self.p2

    def getDistance(self):
        result = math.sqrt(abs(math.pow((self.p1.x - self.p2.x), 2) +
                               pow((self.p1.y - self.p2.y), 2)))
        # print("Distance between " + str(self.p1) +
        #      " and " + str(self.p2) + " is " + str(result))
        return result


class FlapCircle:
    def __init__(self, radius, centerPoint):
        self.radius = radius
        self.centerPoint = centerPoint

    def getCenterPoint(self):
        return self.centerPoint

    def getRadius(self):
        return self.radius

    def drawCircle(self, scene, centerPoint, radius):
        """ reimplement once the core is being settled"""
        pass


class Rect:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height


class OverlappingRectangle(Rect):
    def __init__(self, x, y):
        super().__init__(x, y)


class MarginRectangle(Rect):
    def __init__(self, x, y):
        super().__init__(x, y)


class Calculator:
    def __init__(self):
        pass

    def checkIfCirclesOverlapped(self, circle1, circle2):
        distBetCentres = Line(Point(circle1.getCenterPoint().getX(), circle1.getCenterPoint().getY()), Point(
            circle2.getCenterPoint().getX(), circle2.getCenterPoint().getY())).getDistance()

        return distBetCentres < (circle1.getRadius() + circle2.getRadius())

    def checkIfBoxOverlapped(self, circle1, circle2):

        d = circle1.getRadius() + circle2.getRadius()
        s1 = abs(circle1.getCenterPoint().getX() -
                 circle2.getCenterPoint().getX())
        s2 = abs(circle2.getCenterPoint().getY() -
                 circle1.getCenterPoint().getY())
        print("d , s1 , s2 , rad1 , rad2: ", d, s1, s2,
              circle1.getRadius(), circle2.getRadius())
        print("d : " + str(d))
        o1 = abs(d - s1)
        o2 = abs(d - s2)
        if o1 > 0 and o2 > 0:
            print("OR : (" + str(o1) + "," + str(o2) + ")")
            return OverlappingRectangle(o1, o2)
        else:
            return False

    def getDistance(self, p1, p2):
        result = math.sqrt(abs(math.pow((p1.x - p2.x), 2) +
                               pow((p1.y - p2.y), 2)))
        return result


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
        self.view.setGeometry(0, 0, 1920, 1080)
        self.grayColor = QColor()
        self.grayColor.setRgb(0x252525)
        self.scene.setBackgroundBrush(self.grayColor)

        # Testing
        self.calculator = Calculator()
        rad1 = random.randint(1, 17)
        rad2 = random.randint(1, 17)
        self.drawGrid(0, 0)
        centerPoint1 = Point(0, 0)

        centerPoint2 = Point(0, 0)
        print("sdfg", self.calculator.checkIfBoxOverlapped(
            FlapCircle(rad2, centerPoint2), FlapCircle(rad1, centerPoint1)))

        overlappingRectangle = ""
        while True:
            # Here is to the generation of the random test cases that we wanna try
            """
            After deciding on two of the radiuses, let the 2 circles centers start from the same place
            for the generation, the radius of one of the circles would shift either up or down and check that the circles do not overlap
            if the circles do not overlap , that that there should still be an overlapping rectangle
            if there is no overlapping rectange while there is no overlapping of circles, then it fails the generation and it shoudl restart
            if there is overlapping rectangle with no overlapping circles, then it passes the test
            """

            if self.calculator.checkIfCirclesOverlapped(FlapCircle(rad2, centerPoint2), FlapCircle(rad1, centerPoint1)) == True:
                if random.randint(0, 100) % 2 != 0:
                    # go down
                    centerPoint2.setY(centerPoint2.getY() + 1)
                else:
                    centerPoint2.setX(centerPoint2.getX() + 1)
            else:
                overlappingRectangle = self.calculator.checkIfBoxOverlapped(
                    FlapCircle(rad2, centerPoint2), FlapCircle(rad1, centerPoint1))
                if overlappingRectangle == False:
                    # restart again
                    centerPoint2.setX(0)
                    centerPoint2.setY(0)
                    rad1 = random.randint(1, 10)
                    rad2 = random.randint(1, 10)
                else:
                    break

            # self.drawGrid(x, y)
        print("sdfg", self.calculator.checkIfBoxOverlapped(
            FlapCircle(rad2, centerPoint2), FlapCircle(rad1, centerPoint1)))
        self.drawGrid(max(centerPoint1.getX(), centerPoint2.getX()), max(
            centerPoint1.getY(), centerPoint2.getY()))
        self.plotPoint(centerPoint1)
        self.plotPoint(centerPoint2)
        self.drawCircle(centerPoint1, rad1)
        self.drawCircle(centerPoint2, rad2)

        """
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
        self.gridPixWidth = 18
        self.gridPixHeight = 18
        self.totalPixHeight = self.gridPixHeight * nY
        self.totalPixWidth = self.gridPixWidth * nX

        for i in range(nY+1):
            self.scene.addLine(0, i*self.gridPixHeight,
                               self.totalPixWidth, i*self.gridPixHeight, self.whitePen)
        for i in range(nX+1):
            self.scene.addLine(i*self.gridPixWidth, 0,
                               i*self.gridPixWidth, self.totalPixHeight, self.whitePen)

        """
        self.line = self.scene.addLine(10, 10, 200, 200, self.blackPen)
        self.view.setMaximumWidth(600)
        self.view.setMaximumHeight(600)
        self.line.setFlag(QGraphicsItem.ItemIsMovable)
        """

    def plotPoint(self, point):
        pointRadius = min(self.gridPixHeight, self.gridPixWidth)*0.3
        print(pointRadius)
        self.scene.addEllipse(point.x * self.gridPixWidth - (pointRadius/2), point.y*self.gridPixHeight - (pointRadius/2), pointRadius,
                              pointRadius, self.greenPen)

    def drawStraightLine(self, line, pen):

        test = self.scene.addLine(line.getP1().getX()*self.gridPixWidth, line.getP1().getY() * self.gridPixHeight,
                                  line.getP2().getX()*self.gridPixWidth, line.getP2().getY()*self.gridPixHeight, pen)

        return test

    def drawCircle(self, centerPoint, radius):

        radius = math.ceil(radius)
        diameter = radius*2
        print("x : " + str(centerPoint.getX() - radius))
        print("Diameter : " + str(diameter))
        print("Radius : " + str(radius))
        circle = self.scene.addEllipse(
            (centerPoint.getX()-radius)*self.gridPixWidth, (centerPoint.getY() - radius)*self.gridPixHeight, diameter * self.gridPixWidth, diameter * self.gridPixHeight, self.greenPen)

        return circle

    def reinit(self):
        self.initWindow()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
