#include <QtWidgets/QPushButton>
#include <maya/MGlobal.h>
#include <QtWidgets/QWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QFrame>

#include "dialog.h"
#include "interface/widgets/CollapsibleContainer.h"

USDExportInterface::USDExportInterface(QWidget* parent)
{
    setWindowTitle("Maya USD Export");


    QVBoxLayout *mainLayout = new QVBoxLayout();
    mainLayout->setAlignment(Qt::AlignTop);

    QWidget *mainWidget = new QWidget();
    mainWidget->setLayout(mainLayout);

    auto *scroll = this;
    scroll->setFrameShape(QFrame::NoFrame);

    // add form items
    CollapsibleContainer *generalOptionsContainer = new CollapsibleContainer("General Options", this);
    generalOptionsContainer->addWidget(new QPushButton("world"));
    mainLayout->addWidget(generalOptionsContainer);

    // auto *generalOptionsContainer = CollapsibleContainer("General Options");
    // mainLayout->addWidget(button1);

    scroll->setWidget(mainWidget);

}

// USDExportInterface::USDExportInterface(const QString& text, QWidget* parent)
//     : QScrollArea(parent)
// {
//     setWindowTitle("Maya USD Export");

//     QWidget *mainWidget = new QWidget;
//     auto *mainLayout = new QVBoxLayout();
//     mainWidget->setLayout(mainLayout);
//     mainLayout->setAlignment(Qt::AlignTop);

//     auto b1 = new QPushButton("One");
//     auto b2 = new QPushButton("Two");
//     auto b3 = new QPushButton("Three");

//     mainLayout->addWidget(b1);
//     mainLayout->addWidget(b2);
//     mainLayout->addWidget(b3);

//     this->setWidget(mainWidget);
// }
