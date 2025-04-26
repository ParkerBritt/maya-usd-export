#pragma once

#include "QtCore/qobjectdefs.h"
#include "QtWidgets/qpushbutton.h"
#include <QtWidgets/QWidget>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QComboBox>

class GeneralOptions : public QWidget
{
    Q_OBJECT
public:
    GeneralOptions(QWidget* parent = nullptr);

    QFormLayout *m_formLayout;
    QLineEdit *m_filePathLine;
    QPushButton *m_filePathButton;
    QPushButton *m_exportAssetButton;
    QComboBox *m_fileTypeCombo;
    std::string m_fileOutputPath;

private:

private slots:
    void openFileDialog();
};
