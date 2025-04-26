#include "interface/widgets/CollapsibleContainer.h"
#include "QtCore/qnamespace.h"
#include "QtWidgets/qboxlayout.h"
#include "QtWidgets/qpushbutton.h"
#include "QtWidgets/qwidget.h"
#include <iostream>

#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QPushButton>


CollapsibleContainer::CollapsibleContainer(const QString& _title, QWidget* _parent)
{
    m_mainLayout = new QVBoxLayout();
    m_mainLayout->setAlignment(Qt::AlignTop);
    this->setLayout(m_mainLayout);

    m_headButton = new QPushButton("    "+_title);
    QObject::connect(m_headButton, &QPushButton::clicked, this, &CollapsibleContainer::headerClickedSlot);
    m_headButton->setIcon(QIcon(":/icons/collapse_arrow_down.png"));
    m_headButton->setStyleSheet("text-align:left;");


    m_mainLayout->addWidget(m_headButton);

    m_contentsWidget = new QWidget();
    m_mainLayout->addWidget(m_contentsWidget);
    m_contentsLayout = new QVBoxLayout(m_contentsWidget);
    m_contentsLayout->setContentsMargins(0,0,0,0);
}

void CollapsibleContainer::addWidget(QWidget *_widget)
{
    m_contentsLayout->addWidget(_widget);
}
void CollapsibleContainer::addLayout(QLayout *_layout)
{
    m_contentsLayout->addLayout(_layout);
}

void CollapsibleContainer::headerClickedSlot()
{

    m_contentsWidget->setVisible(! m_contentsWidget->isVisible());
    if(m_contentsWidget->isVisible())
    {
        // TODO: set icon down
        m_headButton->setIcon(QIcon(":/icons/collapse_arrow_down.png"));
    }
    else
    {
        // TODO: set icon right
        m_headButton->setIcon(QIcon(":/icons/collapse_arrow_right.png"));
    }
}
