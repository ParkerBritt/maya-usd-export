#pragma once
#include <QtWidgets/QPushButton>
#include <QtWidgets/QWidget>
#include <QtWidgets/QScrollArea>

class USDExportInterface : public QScrollArea
{
    Q_OBJECT
public:
    USDExportInterface(const QString& text, QWidget* parent = nullptr);
};

