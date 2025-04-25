#pragma once
#include <QtWidgets/QPushButton>
#include <QtWidgets/QWidget>

class USDExportInterface : public QWidget
{
    Q_OBJECT
public:
    USDExportInterface(const QString& text, QWidget* parent = nullptr);
};

