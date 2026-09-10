import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from core import analyze_product


# =========================================================
# Worker Thread
# =========================================================

class Worker(QThread):

    result = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(
        self,
        business,
        product,
        description,
        intended_use,
        target_market,
        existing_certification,
    ):
        super().__init__()

        self.business = business
        self.product = product
        self.description = description
        self.intended_use = intended_use
        self.target_market = target_market
        self.existing_certification = existing_certification

    def run(self):

        try:
            result = analyze_product(
                self.business,
                self.product,
                self.description,
                self.intended_use,
                self.target_market,
                self.existing_certification,
            )

            self.result.emit(result)

        except Exception as e:
            self.error.emit(str(e))


# =========================================================
# Result Card
# =========================================================

class ResultCard(QFrame):

    def __init__(self, title, content, large=False):

        super().__init__()

        self.setObjectName("resultCard")

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        # Title

        title_label = QLabel(title)

        title_label.setObjectName("cardTitle")

        layout.addWidget(title_label)

        # Content

        content_label = QLabel(content)

        content_label.setObjectName("cardContent")

        content_label.setWordWrap(True)

        content_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        layout.addWidget(content_label)

        self.setLayout(layout)


# =========================================================
# BIS Assistant
# =========================================================

class BISAssistant(QWidget):

    def __init__(self):

        super().__init__()

        self.worker = None

        self.setWindowTitle(
            "BIS Standards AI Assistant"
        )

        self.setMinimumSize(1200, 750)

        self.setup_ui()

    # =====================================================
    # UI
    # =====================================================

    def setup_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            24, 20, 24, 20
        )

        main_layout.setSpacing(16)

        # =================================================
        # HEADER
        # =================================================

        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)

        title = QLabel(
            "BIS Standards AI Assistant"
        )

        title.setObjectName("mainTitle")

        subtitle = QLabel(
            "AI-powered guidance for Indian Standards & BIS compliance"
        )

        subtitle.setObjectName("subtitle")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header_layout.addLayout(title_layout)

        header_layout.addStretch()

        self.status_label = QLabel("Ready")

        self.status_label.setObjectName(
            "statusLabel"
        )

        header_layout.addWidget(
            self.status_label,
            alignment=Qt.AlignmentFlag.AlignTop
        )

        main_layout.addLayout(header_layout)

        # =================================================
        # MAIN AREA
        # =================================================

        content_layout = QHBoxLayout()
        content_layout.setSpacing(18)

        # =================================================
        # LEFT PANEL
        # =================================================

        input_panel = QFrame()

        input_panel.setObjectName(
            "inputPanel"
        )

        input_panel.setFixedWidth(350)

        input_layout = QVBoxLayout()

        input_layout.setContentsMargins(
            20, 20, 20, 20
        )

        input_layout.setSpacing(12)

        input_title = QLabel(
            "Product Information"
        )

        input_title.setObjectName(
            "sectionTitle"
        )

        input_layout.addWidget(
            input_title
        )

        input_hint = QLabel(
            "Provide details about the business and product "
            "to identify relevant BIS requirements."
        )

        input_hint.setWordWrap(True)

        input_hint.setObjectName(
            "inputHint"
        )

        input_layout.addWidget(
            input_hint
        )

        # Business

        input_layout.addWidget(
            self.create_label("Business / Industry")
        )

        self.business_input = QLineEdit()

        self.business_input.setPlaceholderText(
            "e.g. Electrical manufacturing"
        )

        input_layout.addWidget(
            self.business_input
        )

        # Product

        input_layout.addWidget(
            self.create_label("Product")
        )

        self.product_input = QLineEdit()

        self.product_input.setPlaceholderText(
            "e.g. Electric water heater"
        )

        input_layout.addWidget(
            self.product_input
        )

        # Description

        input_layout.addWidget(
            self.create_label("Product Description")
        )

        self.description_input = QTextEdit()

        self.description_input.setPlaceholderText(
            "Briefly describe the product..."
        )

        self.description_input.setMaximumHeight(
            90
        )

        input_layout.addWidget(
            self.description_input
        )

        # Intended use

        input_layout.addWidget(
            self.create_label("Intended Use")
        )

        self.use_input = QLineEdit()

        self.use_input.setPlaceholderText(
            "e.g. Residential use"
        )

        input_layout.addWidget(
            self.use_input
        )

        # Target market

        input_layout.addWidget(
            self.create_label("Target Market")
        )

        self.market_input = QLineEdit()

        self.market_input.setText("India")

        input_layout.addWidget(
            self.market_input
        )

        # Existing certification

        input_layout.addWidget(
            self.create_label(
                "Existing Certification (Optional)"
            )
        )

        self.cert_input = QLineEdit()

        self.cert_input.setPlaceholderText(
            "e.g. ISO 9001"
        )

        input_layout.addWidget(
            self.cert_input
        )

        input_layout.addStretch()

        # Analyze button

        self.analyze_button = QPushButton(
            "Analyze Product"
        )

        self.analyze_button.setObjectName(
            "analyzeButton"
        )

        self.analyze_button.setMinimumHeight(
            48
        )

        self.analyze_button.clicked.connect(
            self.analyze
        )

        input_layout.addWidget(
            self.analyze_button
        )

        input_panel.setLayout(
            input_layout
        )

        content_layout.addWidget(
            input_panel
        )

        # =================================================
        # RIGHT RESULTS AREA
        # =================================================

        results_container = QFrame()

        results_container.setObjectName(
            "resultsContainer"
        )

        results_outer_layout = QVBoxLayout()

        results_outer_layout.setContentsMargins(
            0, 0, 0, 0
        )

        results_title = QLabel(
            "Compliance Analysis"
        )

        results_title.setObjectName(
            "resultsTitle"
        )

        results_outer_layout.addWidget(
            results_title
        )

        # Scroll

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.results_widget = QWidget()

        self.results_layout = QGridLayout()

        self.results_layout.setContentsMargins(
            0, 10, 10, 10
        )

        self.results_layout.setHorizontalSpacing(
            14
        )

        self.results_layout.setVerticalSpacing(
            14
        )

        self.results_widget.setLayout(
            self.results_layout
        )

        self.scroll.setWidget(
            self.results_widget
        )

        results_outer_layout.addWidget(
            self.scroll
        )

        results_container.setLayout(
            results_outer_layout
        )

        content_layout.addWidget(
            results_container,
            stretch=1
        )

        main_layout.addLayout(
            content_layout,
            stretch=1
        )

        self.setLayout(
            main_layout
        )

        self.apply_styles()

    # =====================================================
    # Label Helper
    # =====================================================

    def create_label(self, text):

        label = QLabel(text)

        label.setObjectName(
            "inputLabel"
        )

        return label

    # =====================================================
    # Styles
    # =====================================================

    def apply_styles(self):

        self.setStyleSheet("""

            QWidget {
                font-family: Arial;
                font-size: 14px;
                background: #f5f6f8;
                color: #202124;
            }

            /* Header */

            #mainTitle {
                font-size: 27px;
                font-weight: 700;
                background: transparent;
            }

            #subtitle {
                font-size: 13px;
                color: #70757a;
                background: transparent;
            }

            #statusLabel {
                color: #70757a;
                background: transparent;
                padding: 6px 12px;
            }

            /* Input panel */

            #inputPanel {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
            }

            #sectionTitle {
                font-size: 19px;
                font-weight: 700;
                background: transparent;
            }

            #inputHint {
                color: #777;
                font-size: 12px;
                background: transparent;
                padding-bottom: 6px;
            }

            #inputLabel {
                font-size: 12px;
                font-weight: 600;
                color: #555;
                background: transparent;
            }

            QLineEdit,
            QTextEdit {

                background: #fafafa;

                border: 1px solid #d5d5d5;

                border-radius: 6px;

                padding: 9px;

                color: #222;
            }

            QLineEdit:focus,
            QTextEdit:focus {

                border: 1px solid #555;

                background: white;
            }

            /* Analyze button */

            #analyzeButton {

                background: #222;

                color: white;

                border: none;

                border-radius: 7px;

                font-size: 14px;

                font-weight: 600;
            }

            #analyzeButton:hover {
                background: #444;
            }

            #analyzeButton:disabled {
                background: #999;
            }

            /* Results */

            #resultsContainer {
                background: transparent;
            }

            #resultsTitle {
                font-size: 19px;
                font-weight: 700;
                background: transparent;
            }

            #resultCard {

                background: white;

                border: 1px solid #dedede;

                border-radius: 10px;
            }

            #cardTitle {

                font-size: 17px;

                font-weight: 700;

                background: transparent;

                padding-bottom: 3px;
            }

            #cardContent {

                font-size: 13px;

                line-height: 1.5;

                color: #444;

                background: transparent;
            }

            QScrollArea {
                background: transparent;
                border: none;
            }

        """)

    # =====================================================
    # Analyze
    # =====================================================

    def analyze(self):

        business = self.business_input.text().strip()

        product = self.product_input.text().strip()

        description = (
            self.description_input
            .toPlainText()
            .strip()
        )

        intended_use = (
            self.use_input.text()
            .strip()
        )

        target_market = (
            self.market_input.text()
            .strip()
        )

        certification = (
            self.cert_input.text()
            .strip()
        )

        if not business or not product:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter at least the business and product."
            )

            return

        self.analyze_button.setEnabled(
            False
        )

        self.status_label.setText(
            "Analyzing..."
        )

        self.clear_results()

        self.worker = Worker(
            business,
            product,
            description,
            intended_use,
            target_market,
            certification,
        )

        self.worker.result.connect(
            self.display_results
        )

        self.worker.error.connect(
            self.display_error
        )

        self.worker.start()

    # =====================================================
    # Display Results
    # =====================================================

    def display_results(self, data):

        # Summary - full width

        summary = data.get(
            "summary",
            "No summary available."
        )

        self.add_card(
            "📌 Executive Summary",
            summary,
            0,
            0,
            2
        )

        # Standards - full width

        standards = data.get(
            "standards",
            []
        )

        standards_text = ""

        for standard in standards:

            standards_text += (
                f"• {standard.get('name', 'Unknown')}\n"
                f"  {standard.get('title', '')}\n"
                f"  {standard.get('relevance', '')}\n"
                f"  Mandatory: "
                f"{standard.get('mandatory', 'Needs verification')}\n\n"
            )

        if not standards_text:

            standards_text = (
                "No specific standards identified. "
                "Verification with official BIS sources is recommended."
            )

        self.add_card(
            "📋 Applicable Standards",
            standards_text,
            1,
            0,
            2
        )

        # Certification

        certification = data.get(
            "certification",
            {}
        )

        certification_text = (
            f"Required: "
            f"{certification.get('required', 'Unknown')}\n\n"
            f"Scheme: "
            f"{certification.get('scheme', 'Not specified')}\n\n"
            f"{certification.get('details', '')}"
        )

        self.add_card(
            "🏷 BIS Certification",
            certification_text,
            2,
            0,
            1
        )

        # Process

        process = data.get(
            "process",
            []
        )

        process_text = "\n".join(
            f"{i + 1}. {step}"
            for i, step in enumerate(process)
        )

        if not process_text:
            process_text = "No process information available."

        self.add_card(
            "📑 Certification Process",
            process_text,
            2,
            1,
            1
        )

        # Testing

        testing = data.get(
            "testing",
            []
        )

        testing_text = "\n".join(
            f"• {item}"
            for item in testing
        )

        if not testing_text:
            testing_text = "No testing information available."

        self.add_card(
            "🔬 Testing Requirements",
            testing_text,
            3,
            0,
            1
        )

        # Documents

        documents = data.get(
            "documents",
            []
        )

        documents_text = "\n".join(
            f"• {item}"
            for item in documents
        )

        if not documents_text:
            documents_text = "No document information available."

        self.add_card(
            "📁 Required Documents",
            documents_text,
            3,
            1,
            1
        )

        # Additional requirements

        additional = data.get(
            "additional_requirements",
            []
        )

        if additional:

            additional_text = "\n".join(
                f"• {item}"
                for item in additional
            )

            self.add_card(
                "⚙ Additional Requirements",
                additional_text,
                4,
                0,
                1
            )

        # Warnings

        warnings = data.get(
            "warnings",
            []
        )

        if warnings:

            warnings_text = "\n".join(
                f"⚠ {item}"
                for item in warnings
            )

            self.add_card(
                "⚠ Important Notes",
                warnings_text,
                4,
                1,
                1
            )

        self.results_layout.setRowStretch(
            self.results_layout.rowCount(),
            1
        )

        self.status_label.setText(
            "Analysis complete"
        )

        self.analyze_button.setEnabled(
            True
        )

    # =====================================================
    # Add Card
    # =====================================================

    def add_card(
        self,
        title,
        content,
        row,
        column,
        column_span=1
    ):

        card = ResultCard(
            title,
            content
        )

        self.results_layout.addWidget(
            card,
            row,
            column,
            1,
            column_span
        )

    # =====================================================
    # Clear Results
    # =====================================================

    def clear_results(self):

        while self.results_layout.count():

            item = self.results_layout.takeAt(0)

            widget = item.widget()

            if widget:

                widget.deleteLater()

    # =====================================================
    # Error
    # =====================================================

    def display_error(self, error):

        self.clear_results()

        self.add_card(
            "❌ Error",
            error,
            0,
            0,
            2
        )

        self.status_label.setText(
            "Analysis failed"
        )

        self.analyze_button.setEnabled(
            True
        )


# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = BISAssistant()

    window.show()

    sys.exit(
        app.exec()
    )