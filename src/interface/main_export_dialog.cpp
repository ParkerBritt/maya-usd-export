#include <QtWidgets/QPushButton>
#include <maya/MGlobal.h>
#include <QtWidgets/QWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QFrame>

#include "interface/main_export_dialog.h"
#include "QtWidgets/qboxlayout.h"
#include "QtWidgets/qpushbutton.h"
#include "interface/widgets/CollapsibleContainer.h"
#include "interface/widgets/GeneralOptions.h"
#include "interface/widgets/SelectionOptions.h"
#include "interface/widgets/AnimationOptions.h"

USDExportInterface::USDExportInterface(QWidget* parent)
{
    setWindowTitle("Maya USD Export");
    setAttribute(Qt::WA_DeleteOnClose);



    initUI();

    auto *scroll = this;
    scroll->setFrameShape(QFrame::NoFrame);
    this->resize(m_mainWidget->minimumSizeHint().width()*2, m_mainWidget->minimumSizeHint().width()*3);
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
    this->generalOptions = new GeneralOptions();
    generalOptionsContainer->addWidget(this->generalOptions);
    m_mainLayout->addWidget(generalOptionsContainer);

    CollapsibleContainer *selectionOptionsContainer = new CollapsibleContainer("Selection Options", this);
    this->selectionOptions = new SelectionOptions();
    selectionOptionsContainer->addWidget(this->selectionOptions);
    m_mainLayout->addWidget(selectionOptionsContainer);

    CollapsibleContainer *animationOptionsContainer = new CollapsibleContainer("Animation Options", this);
    this->animationOptions = new AnimationOptions();
    animationOptionsContainer->addWidget(this->animationOptions);
    m_mainLayout->addWidget(animationOptionsContainer);

    auto *footerButtonsLayout = new QHBoxLayout();
    footerButtonsLayout->addStretch();
    m_exportButton = new QPushButton("Export");
    m_cancelButton = new QPushButton("Cancel");
    // close window
    connect(m_cancelButton, &QPushButton::clicked, this, &USDExportInterface::close); 
    footerButtonsLayout->addWidget(m_exportButton);
    footerButtonsLayout->addWidget(m_cancelButton);
    m_mainLayout->addStretch();
    m_mainLayout->addLayout(footerButtonsLayout);
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
