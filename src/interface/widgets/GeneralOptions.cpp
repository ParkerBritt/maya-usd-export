#include "interface/widgets/GeneralOptions.h"
#include "QtCore/qnamespace.h"
#include "QtWidgets/qboxlayout.h"
#include "QtWidgets/qformlayout.h"
#include "QtWidgets/qpushbutton.h"
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QSizePolicy>
#include <QtWidgets/QFileDialog>
#include <cstdlib>


GeneralOptions::GeneralOptions(QWidget* parent)
{
    m_formLayout = new QFormLayout();
    setLayout(m_formLayout);
    m_formLayout->setLabelAlignment(Qt::AlignLeft | Qt::AlignVCenter);

    // default export path
    m_fileOutputPath = std::getenv("HOME"); 
    auto *filePathLayout = new QHBoxLayout(); 
    m_filePathLine = new QLineEdit(m_fileOutputPath.c_str());

    m_filePathButton = new QPushButton("Change");
    connect(m_filePathButton, &QPushButton::clicked, this, &GeneralOptions::openFileDialog);
    filePathLayout->addWidget(m_filePathLine);     
    filePathLayout->addWidget(m_filePathButton);     


    m_fileTypeCombo = new QComboBox(); 
    m_fileTypeCombo->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
    m_fileTypeCombo->addItem("USD");
    m_fileTypeCombo->addItem("Alembic");

    m_formLayout->addRow("File Path", filePathLayout);
}

void GeneralOptions::openFileDialog()
{
    QString filePath = QFileDialog::getSaveFileName(this, "Save File", m_fileOutputPath.c_str(), tr("USD Files (*.usd *.usda *.usdc)"));
    // TODO: add validation
    bool isValid = true;
    if(isValid && filePath.length()>0)
    {
        m_filePathLine->setText(filePath);
        m_fileOutputPath = filePath.toStdString();
    }
}
