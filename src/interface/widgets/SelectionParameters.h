#pragma once

#include "QtCore/qobjectdefs.h"
#include "QtWidgets/qformlayout.h"
#include <QtWidgets/QWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QFormLayout>


class SelectionParameters
: public QWidget
{
    Q_OBJECT
public:
    SelectionParameters();
private:
    QVBoxLayout* mainLayout_;
    QFormLayout* formLayout_;
};
