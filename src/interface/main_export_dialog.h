#pragma once
#include <QtWidgets/QPushButton>
#include <QtWidgets/QWidget>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QBoxLayout>

class USDExportInterface : public QScrollArea
{
    Q_OBJECT
public:
    USDExportInterface(QWidget* parent = nullptr);

    QBoxLayout *m_mainLayout;
    QWidget *m_mainWidget;

    QPushButton *m_exportButton;
    QPushButton *m_cancelButton;

private:
    void initUI();
};

