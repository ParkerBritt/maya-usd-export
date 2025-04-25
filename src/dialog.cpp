#include <QtWidgets/QPushButton>
#include <maya/MGlobal.h>
#include <QtWidgets/QWidget>
#include <QtWidgets/QVBoxLayout>
#include "dialog.h"

USDExportInterface::USDExportInterface(const QString& text, QWidget* parent)
    : QWidget(parent)
{
    QPushButton *button1 = new QPushButton("One");
    QPushButton *button2 = new QPushButton("Two");
    QPushButton *button3 = new QPushButton("Three");
    QPushButton *button4 = new QPushButton("Four");
    QPushButton *button5 = new QPushButton("Five");

    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->addWidget(button1);
    mainLayout->addWidget(button2);
    mainLayout->addWidget(button3);
    mainLayout->addWidget(button4);
    mainLayout->addWidget(button5);
}

