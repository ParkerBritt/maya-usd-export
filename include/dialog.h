#pragma once
#include <QtWidgets/QPushButton>
#include <QtWidgets/QWidget>
#include <QtWidgets/QScrollArea>

class USDExportInterface : public QScrollArea
{
    Q_OBJECT
public:
    USDExportInterface(QWidget* parent = nullptr);
};

