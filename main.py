import sys
import math

from PyQt6.QtCore import Qt, QTimer, QPoint, QPointF
from PyQt6.QtGui import (
    QPainter,
    QPen,
    QBrush,
    QColor,
    QPolygonF,
    QPixmap
)
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMenu,
    QFileDialog
)


class LuckyDangle(QWidget):

    def __init__(self):
        super().__init__()

        # ==========================================
        # WINDOW SETTINGS
        # ==========================================

        self.WIDTH = 200
        self.HEIGHT = 320

        self.setFixedSize(
            self.WIDTH,
            self.HEIGHT
        )

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        # ==========================================
        # CHARM SETTINGS
        # ==========================================

        self.current_charm = "clover"

        # Path of your own image
        self.custom_image_path = ""

        # ==========================================
        # PHYSICS
        # ==========================================

        self.angle = 0.20
        self.velocity = 0.0

        self.gravity = 0.0025
        self.spring = 0.0015
        self.damping = 0.992

        # ==========================================
        # DRAGGING
        # ==========================================

        self.dragging = False

        self.drag_position = QPoint()

        self.previous_mouse_position = None

        # ==========================================
        # START POSITION - TOP RIGHT
        # ==========================================

        screen = (
            QApplication
            .primaryScreen()
            .availableGeometry()
        )

        x = (
            screen.right()
            - self.WIDTH
            - 20
        )

        y = (
            screen.top()
            + 20
        )

        self.move(x, y)

        # ==========================================
        # ANIMATION
        # ==========================================

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.update_physics
        )

        self.timer.start(16)

    # =================================================
    # PHYSICS
    # =================================================

    def update_physics(self):

        if self.dragging:
            return

        acceleration = (
            -self.spring * self.angle
            -self.gravity * math.sin(self.angle)
        )

        self.velocity += acceleration

        self.velocity *= self.damping

        self.angle += self.velocity

        # Maximum swing angle

        max_angle = 0.75

        if self.angle > max_angle:

            self.angle = max_angle

            self.velocity *= -0.5

        if self.angle < -max_angle:

            self.angle = -max_angle

            self.velocity *= -0.5

        self.update()

    # =================================================
    # PAINT EVENT
    # =================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        # ==========================================
        # ANCHOR
        # ==========================================

        anchor_x = self.WIDTH // 2
        anchor_y = 0

        # ==========================================
        # STRING
        # ==========================================

        string_length = 145

        end_x = (
            anchor_x
            + math.sin(self.angle)
            * string_length
        )

        end_y = (
            anchor_y
            + math.cos(self.angle)
            * string_length
        )

        # ==========================================
        # DRAW STRING
        # ==========================================

        pen = QPen(
            QColor("#B8893C")
        )

        pen.setWidth(3)

        painter.setPen(pen)

        painter.drawLine(
            anchor_x,
            anchor_y,
            int(end_x),
            int(end_y)
        )

        # ==========================================
        # FIRST WHITE BEAD
        # ==========================================

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            QBrush(
                QColor("#F5F5F5")
            )
        )

        painter.drawEllipse(
            int(end_x - 8),
            int(end_y - 8),
            16,
            16
        )

        # ==========================================
        # SECOND BEAD
        # ==========================================

        bead_distance = 25

        bead_x = (
            end_x
            + math.sin(self.angle)
            * bead_distance
        )

        bead_y = (
            end_y
            + math.cos(self.angle)
            * bead_distance
        )

        painter.drawEllipse(
            int(bead_x - 7),
            int(bead_y - 7),
            14,
            14
        )

        # ==========================================
        # CHARM POSITION
        # ==========================================

        charm_distance = 50

        charm_x = (
            end_x
            + math.sin(self.angle)
            * charm_distance
        )

        charm_y = (
            end_y
            + math.cos(self.angle)
            * charm_distance
        )

        # ==========================================
        # DRAW SELECTED CHARM
        # ==========================================

        if self.current_charm == "clover":

            self.draw_clover(
                painter,
                charm_x,
                charm_y
            )

        elif self.current_charm == "star":

            self.draw_star(
                painter,
                charm_x,
                charm_y
            )

        elif self.current_charm == "heart":

            self.draw_heart(
                painter,
                charm_x,
                charm_y
            )

        elif self.current_charm == "moon":

            self.draw_moon(
                painter,
                charm_x,
                charm_y
            )

        elif self.current_charm == "flower":

            self.draw_flower(
                painter,
                charm_x,
                charm_y
            )

        elif self.current_charm == "custom":

            self.draw_custom_image(
                painter,
                charm_x,
                charm_y
            )

        painter.end()

    # =================================================
    # CLOVER
    # =================================================

    def draw_clover(
        self,
        painter,
        x,
        y
    ):

        painter.save()

        painter.translate(x, y)

        painter.rotate(
            math.degrees(self.angle)
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            QBrush(
                QColor("#70C91A")
            )
        )

        positions = [
            (-22, -22),
            (22, -22),
            (-22, 22),
            (22, 22)
        ]

        for px, py in positions:

            painter.drawEllipse(
                px - 25,
                py - 25,
                50,
                50
            )

        # Inner highlights

        painter.setBrush(
            QBrush(
                QColor("#A5E63A")
            )
        )

        for px, py in positions:

            painter.drawEllipse(
                px - 11,
                py - 11,
                22,
                22
            )

        # Center

        painter.setBrush(
            QBrush(
                QColor("#5EAD16")
            )
        )

        painter.drawEllipse(
            -10,
            -10,
            20,
            20
        )

        # Stem

        pen = QPen(
            QColor("#5EAD16")
        )

        pen.setWidth(7)

        painter.setPen(pen)

        painter.drawLine(
            0,
            25,
            10,
            65
        )

        painter.restore()

    # =================================================
    # STAR
    # =================================================

    def draw_star(
        self,
        painter,
        x,
        y
    ):

        painter.save()

        painter.translate(x, y)

        painter.rotate(
            math.degrees(self.angle)
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            QBrush(
                QColor("#FFD43B")
            )
        )

        points = []

        for i in range(10):

            radius = (
                38
                if i % 2 == 0
                else 17
            )

            angle = (
                -math.pi / 2
                + i * math.pi / 5
            )

            px = math.cos(angle) * radius
            py = math.sin(angle) * radius

            # IMPORTANT:
            # QPolygonF needs QPointF

            points.append(
                QPointF(px, py)
            )

        polygon = QPolygonF(points)

        painter.drawPolygon(
            polygon
        )

        painter.restore()

    # =================================================
    # HEART
    # =================================================

    def draw_heart(
        self,
        painter,
        x,
        y
    ):

        painter.save()

        painter.translate(x, y)

        painter.rotate(
            math.degrees(self.angle)
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            QBrush(
                QColor("#F0445E")
            )
        )

        # Left top

        painter.drawEllipse(
            -35,
            -25,
            40,
            40
        )

        # Right top

        painter.drawEllipse(
            -5,
            -25,
            40,
            40
        )

        # Bottom

        points = QPolygonF([
            QPointF(-35, -5),
            QPointF(35, -5),
            QPointF(0, 45)
        ])

        painter.drawPolygon(
            points
        )

        painter.restore()

    # =================================================
    # MOON
    # =================================================

    def draw_moon(
        self,
        painter,
        x,
        y
    ):

        painter.save()

        painter.translate(x, y)

        painter.rotate(
            math.degrees(self.angle)
        )

        # Draw moon using two circles

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            QBrush(
                QColor("#FFE58A")
            )
        )

        painter.drawEllipse(
            -35,
            -35,
            70,
            70
        )

        # Overlay circle

        painter.setBrush(
            QBrush(
                QColor(30, 30, 30, 0)
            )
        )

        painter.setCompositionMode(
            QPainter.CompositionMode.CompositionMode_Clear
        )

        painter.drawEllipse(
            -5,
            -38,
            60,
            60
        )

        painter.restore()

    # =================================================
    # FLOWER
    # =================================================

    def draw_flower(
        self,
        painter,
        x,
        y
    ):

        painter.save()

        painter.translate(x, y)

        painter.rotate(
            math.degrees(self.angle)
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            QBrush(
                QColor("#FF78C8")
            )
        )

        positions = [
            (0, -25),
            (25, 0),
            (0, 25),
            (-25, 0)
        ]

        for px, py in positions:

            painter.drawEllipse(
                px - 22,
                py - 22,
                44,
                44
            )

        # Center

        painter.setBrush(
            QBrush(
                QColor("#FFD43B")
            )
        )

        painter.drawEllipse(
            -15,
            -15,
            30,
            30
        )

        painter.restore()

    # =================================================
    # CUSTOM IMAGE
    # =================================================

    def draw_custom_image(
        self,
        painter,
        x,
        y
    ):

        # If no image selected

        if not self.custom_image_path:
            return

        pixmap = QPixmap(
            self.custom_image_path
        )

        if pixmap.isNull():
            return

        painter.save()

        painter.translate(x, y)

        painter.rotate(
            math.degrees(self.angle)
        )

        # Resize image

        pixmap = pixmap.scaled(
            75,
            75,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        painter.drawPixmap(
            -pixmap.width() // 2,
            -pixmap.height() // 2,
            pixmap
        )

        painter.restore()

    # =================================================
    # MOUSE PRESS
    # =================================================

    def mousePressEvent(self, event):

        # LEFT CLICK = DRAG

        if event.button() == Qt.MouseButton.LeftButton:

            self.dragging = True

            self.drag_position = (
                event.globalPosition().toPoint()
                -
                self.frameGeometry().topLeft()
            )

            self.previous_mouse_position = (
                event.globalPosition().toPoint()
            )

            self.velocity = 0

            event.accept()

        # RIGHT CLICK = MENU

        elif event.button() == Qt.MouseButton.RightButton:

            self.show_menu(
                event.globalPosition().toPoint()
            )

            event.accept()

    # =================================================
    # MOUSE MOVE
    # =================================================

    def mouseMoveEvent(self, event):

        if self.dragging:

            current_position = (
                event.globalPosition().toPoint()
            )

            # Move charm window

            self.move(
                current_position
                -
                self.drag_position
            )

            # Calculate throwing speed

            if self.previous_mouse_position:

                movement = (
                    current_position
                    -
                    self.previous_mouse_position
                )

                self.velocity = (
                    movement.x() * 0.002
                )

            self.previous_mouse_position = (
                current_position
            )

            self.update()

            event.accept()

    # =================================================
    # MOUSE RELEASE
    # =================================================

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.dragging = False

            self.previous_mouse_position = None

            event.accept()

    # =================================================
    # RIGHT CLICK MENU
    # =================================================

    def show_menu(self, position):

        menu = QMenu()

        menu.setStyleSheet("""
            QMenu {
                background-color: #202124;
                color: white;
                border: 1px solid #555555;
                padding: 5px;
            }

            QMenu::item {
                padding: 8px 25px;
            }

            QMenu::item:selected {
                background-color: #3C4043;
            }
        """)

        # ==========================================
        # CHARM MENU
        # ==========================================

        charm_menu = menu.addMenu(
            "Choose Charm"
        )

        clover_action = charm_menu.addAction(
            "🍀 Clover"
        )

        star_action = charm_menu.addAction(
            "⭐ Star"
        )

        heart_action = charm_menu.addAction(
            "❤️ Heart"
        )

        moon_action = charm_menu.addAction(
            "🌙 Moon"
        )

        flower_action = charm_menu.addAction(
            "🌸 Flower"
        )

        custom_action = charm_menu.addAction(
            "🖼️ Upload My Charm"
        )

        menu.addSeparator()

        # ==========================================
        # EXIT
        # ==========================================

        exit_action = menu.addAction(
            "❌ Exit"
        )

        # ==========================================
        # SHOW MENU
        # ==========================================

        selected = menu.exec(position)

        # ==========================================
        # SELECT CHARM
        # ==========================================

        if selected == clover_action:

            self.current_charm = "clover"

        elif selected == star_action:

            self.current_charm = "star"

        elif selected == heart_action:

            self.current_charm = "heart"

        elif selected == moon_action:

            self.current_charm = "moon"

        elif selected == flower_action:

            self.current_charm = "flower"

        # ==========================================
        # UPLOAD YOUR OWN IMAGE
        # ==========================================

        elif selected == custom_action:

            self.upload_custom_charm()

        # ==========================================
        # EXIT
        # ==========================================

        elif selected == exit_action:

            QApplication.quit()

        self.update()

    # =================================================
    # UPLOAD CUSTOM CHARM
    # =================================================

    def upload_custom_charm(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Your Charm",
            "",
            "Images (*.png *.jpg *.jpeg *.webp)"
        )

        if file_path:

            self.custom_image_path = file_path

            self.current_charm = "custom"

            self.update()


# =====================================================
# START APPLICATION
# =====================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    charm = LuckyDangle()

    charm.show()

    sys.exit(
        app.exec()
    )
    