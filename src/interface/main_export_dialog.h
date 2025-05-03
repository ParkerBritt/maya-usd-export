#pragma once
#include <QtWidgets/QPushButton>
#include <QtWidgets/QWidget>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QBoxLayout>

#include "interface/widgets/GeneralOptions.h"
#include "interface/widgets/SelectionOptions.h"
#include "interface/widgets/AnimationOptions.h"

class USDExportInterface : public QScrollArea
{
    Q_OBJECT
public:
    USDExportInterface(QWidget* parent = nullptr);

    QBoxLayout *m_mainLayout;
    QWidget *m_mainWidget;

    QPushButton *m_exportButton;
    QPushButton *m_cancelButton;

    AnimationOptions* animationOptions;
    GeneralOptions* generalOptions;


private:
    void initUI();
};

