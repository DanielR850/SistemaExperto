from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from logic.imc_calculator import calcular_imc
from logic.rules import clasificar_imc, generar_recomendacion
from logic.db_manager import crear_tabla, guardar_evaluacion

crear_tabla()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Experto de Evaluación IMC")
        self.showMaximized()
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.inputs = {}
        self.resultado_final = ""

        self.section_fields = {
            "Salud Física": ["edad", "peso", "altura"],
            "Salud Médica": ["antecedentes", "medico"],
            "Estilo de Vida": ["ejercicio", "es_sedentario", "fuma", "come_verduras"],
            "Salud Emocional": ["duerme_bien", "duerme_mal", "estresado"]
        }

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()

        self.page1_salud_fisica()
        self.page2_salud_medica()
        self.page3_estilo_vida()
        self.page4_salud_emocional()

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setFixedHeight(300)

        layout.addWidget(self.stacked_widget)
        layout.addWidget(QLabel("Resultado de la Evaluación:"))
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def create_section(self, titulo):
        page = QWidget()
        layout = QVBoxLayout(page)

        titulo_label = QLabel(titulo)
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(titulo_label)

        return page, layout

    def add_question(self, layout, texto, key, tipo="text"):
        fila = QHBoxLayout()
        label = QLabel(texto)
        label.setFixedWidth(300)
        fila.addWidget(label)

        if tipo == "text":
            campo = QLineEdit()
        else:
            campo = QComboBox()
            campo.addItems(["Sí", "No"])
            campo.currentIndexChanged.connect(lambda _, k=key: self.generar_feedback(k))

        campo.setFixedWidth(200)
        self.inputs[key] = campo
        fila.addWidget(campo)
        layout.addLayout(fila)

    def add_navigation(self, layout, siguiente, seccion, finalizar=False):
        boton_layout = QHBoxLayout()
        boton_layout.addStretch()

        if finalizar:
            boton = QPushButton("Finalizar evaluación")
            boton.clicked.connect(self.evaluar)
            boton_layout.addWidget(boton)
        else:
            si_btn = QPushButton("Continuar")
            si_btn.clicked.connect(lambda: self.procesar_seccion(siguiente, seccion))
            no_btn = QPushButton("No continuar")
            no_btn.clicked.connect(self.evaluar)
            boton_layout.addWidget(si_btn)
            boton_layout.addWidget(no_btn)

        boton_layout.addStretch()
        layout.addLayout(boton_layout)

    def generar_feedback(self, key):
        respuestas = {
            "antecedentes": "Se recomienda consultar con un médico periódicamente.",
            "medico": "Buen hábito: continuar con chequeos médicos.",
            "ejercicio": "Excelente, siga con su actividad física.",
            "es_sedentario": "Reduzca el tiempo sedentario con pausas activas.",
            "fuma": "Considere dejar de fumar para mejorar su salud.",
            "come_verduras": "Mantenga su dieta saludable.",
            "duerme_bien": "Continúe con sus buenos hábitos de sueño.",
            "duerme_mal": "Procure dormir mejor para mejorar su salud.",
            "estresado": "Relájese con respiración, meditación o caminatas."
        }
        if isinstance(self.inputs[key], QComboBox):
            if self.inputs[key].currentText() == "Sí":
                sugerencia = respuestas.get(key, "Sin recomendación específica.")
                self.resultado_final += f"\n✔ {sugerencia}"
                self.resultado.setText(self.resultado_final)

    def procesar_seccion(self, siguiente, seccion):
        campos = self.section_fields.get(seccion, [])
        resumen = [f"{campo.replace('_', ' ').capitalize()}: {self.inputs[campo].currentText()}"
                   for campo in campos if isinstance(self.inputs[campo], QComboBox)]
        if resumen:
            self.resultado_final += f"\n{seccion} → " + ", ".join(resumen)
            self.resultado.setText(self.resultado_final)
        self.stacked_widget.setCurrentIndex(siguiente)

    def page1_salud_fisica(self):
        pagina, layout = self.create_section("Salud Física")
        self.add_question(layout, "Edad:", "edad")
        self.add_question(layout, "Peso (kg):", "peso")
        self.add_question(layout, "Altura (m):", "altura")

        boton = QPushButton("Calcular IMC y continuar")
        boton.clicked.connect(self.calcular_imc)
        layout.addWidget(boton, alignment=Qt.AlignCenter)

        self.stacked_widget.addWidget(pagina)

    def calcular_imc(self):
        try:
            edad = int(self.inputs["edad"].text())
            peso = float(self.inputs["peso"].text())
            altura = float(self.inputs["altura"].text())

            imc = calcular_imc(peso, altura)
            clasificacion = clasificar_imc(imc, edad)
            self.inputs["imc"] = imc
            self.inputs["clasificacion"] = clasificacion

            self.resultado_final += f"\nSalud Física → IMC: {imc:.2f} → {clasificacion}"
            self.resultado.setText(self.resultado_final)
            self.stacked_widget.setCurrentIndex(1)

        except ValueError:
            QMessageBox.warning(self, "Error", "Ingrese valores válidos.")

    def page2_salud_medica(self):
        pagina, layout = self.create_section("Salud Médica")
        self.add_question(layout, "¿Tiene antecedentes familiares?", "antecedentes", "combo")
        self.add_question(layout, "¿Fue al médico el último año?", "medico", "combo")
        self.add_navigation(layout, 2, "Salud Médica")
        self.stacked_widget.addWidget(pagina)

    def page3_estilo_vida(self):
        pagina, layout = self.create_section("Estilo de Vida")
        self.add_question(layout, "¿Hace ejercicio regularmente?", "ejercicio", "combo")
        self.add_question(layout, "¿Pasa más de 6 horas al día sentado?", "es_sedentario", "combo")
        self.add_question(layout, "¿Fuma?", "fuma", "combo")
        self.add_question(layout, "¿Consume frutas y verduras diariamente?", "come_verduras", "combo")
        self.add_navigation(layout, 3, "Estilo de Vida")
        self.stacked_widget.addWidget(pagina)

    def page4_salud_emocional(self):
        pagina, layout = self.create_section("Salud Emocional")
        self.add_question(layout, "¿Duerme entre 7 y 9 horas al día?", "duerme_bien", "combo")
        self.add_question(layout, "¿Tiene dificultades para dormir?", "duerme_mal", "combo")
        self.add_question(layout, "¿Se siente estresado con frecuencia?", "estresado", "combo")
        self.add_navigation(layout, 4, "Salud Emocional", finalizar=True)
        self.stacked_widget.addWidget(pagina)

    def evaluar(self):
        try:
            edad = int(self.inputs["edad"].text())
            peso = float(self.inputs["peso"].text())
            altura = float(self.inputs["altura"].text())
            imc = self.inputs["imc"]
            clasificacion = self.inputs["clasificacion"]

            respuestas = {k: self.inputs[k].currentText() == "Sí"
                          for k in self.inputs if isinstance(self.inputs[k], QComboBox)}

            recomendacion = generar_recomendacion(
                clasificacion,
                respuestas.get("fuma", False), respuestas.get("ejercicio", False),
                respuestas.get("antecedentes", False), respuestas.get("medico", False),
                respuestas.get("duerme_bien", False), respuestas.get("come_verduras", False),
                respuestas.get("es_sedentario", False), respuestas.get("duerme_mal", False),
                respuestas.get("estresado", False)
            )

            guardar_evaluacion(
                edad, peso, altura, imc, clasificacion,
                respuestas.get("fuma", False), respuestas.get("ejercicio", False),
                respuestas.get("antecedentes", False), respuestas.get("medico", False),
                respuestas.get("duerme_bien", False), respuestas.get("come_verduras", False),
                respuestas.get("es_sedentario", False), respuestas.get("duerme_mal", False),
                respuestas.get("estresado", False), recomendacion
            )

            self.resultado_final += f"\n\nRecomendación final:\n{recomendacion}"
            self.resultado.setText(self.resultado_final)

        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese valores válidos.")
