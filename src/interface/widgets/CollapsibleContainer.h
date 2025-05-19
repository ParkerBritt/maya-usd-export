#pragma once
#include "QtWidgets/qboxlayout.h"
#include <QtWidgets/QWidget>
#include <QtWidgets/QLayout>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QPushButton>

class CollapsibleContainer : public QWidget
{
    Q_OBJECT
public:
    CollapsibleContainer(const QString& _title, QWidget* _parent = nullptr);

    void addWidget(QWidget *_widget);
    void addLayout(QLayout *_layout);

private slots:
    void headerClickedSlot();

private:
    QVBoxLayout *m_contentsLayout;
    QWidget *m_contentsWidget;

    QVBoxLayout *m_mainLayout;
    QPushButton *m_headButton;
};


