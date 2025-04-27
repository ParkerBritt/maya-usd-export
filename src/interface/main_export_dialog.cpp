#include <QtWidgets/QPushButton>
#include <maya/MGlobal.h>
#include <QtWidgets/QWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QFrame>

#include "interface/main_export_dialog.h"
#include "interface/widgets/CollapsibleContainer.h"
#include "interface/widgets/GeneralOptions.h"

USDExportInterface::USDExportInterface(QWidget* parent)
{
    setWindowTitle("Maya USD Export");



    initUI();

    auto *scroll = this;
    scroll->setFrameShape(QFrame::NoFrame);
    this->resize(m_mainWidget->minimumSizeHint().width()*1.5, m_mainWidget->minimumSizeHint().width()*2);
    scroll->setWidgetResizable(true);
    scroll->setWidget(m_mainWidget);


}

void USDExportInterface::initUI()
{
    m_mainLayout = new QVBoxLayout();
    m_mainLayout->setAlignment(Qt::AlignTop);

    m_mainWidget = new QWidget();
    m_mainWidget->setLayout(m_mainLayout);

    // add form items
    CollapsibleContainer *generalOptionsContainer = new CollapsibleContainer("General Options", this);
    generalOptionsContainer->addWidget(new GeneralOptions());
    m_mainLayout->addWidget(generalOptionsContainer);

    CollapsibleContainer *selectionOptionsContainer = new CollapsibleContainer("Seleciton Options", this);
    selectionOptionsContainer->addWidget(new QPushButton("world"));
    m_mainLayout->addWidget(selectionOptionsContainer);
}

// USDExportInterface::USDExportInterface(const QString& text, QWidget* parent)
//     : QScrollArea(parent)
// {
//     setWindowTitle("Maya USD Export");

//     QWidget *m_mainWidget = new QWidget;
//     auto *m_mainLayout = new QVBoxLayout();
//     m_mainWidget->setLayout(m_mainLayout);
//     m_mainLayout->setAlignment(Qt::AlignTop);

//     auto b1 = new QPushButton("One");
//     auto b2 = new QPushButton("Two");
//     auto b3 = new QPushButton("Three");

//     m_mainLayout->addWidget(b1);
//     m_mainLayout->addWidget(b2);
//     m_mainLayout->addWidget(b3);

//     this->setWidget(m_mainWidget);
// }
