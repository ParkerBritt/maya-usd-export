#include "interface/widgets/SelectionParameters.h"
#include "QtWidgets/qboxlayout.h"
#include <QtWidgets/QLabel>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QLineEdit>

SelectionParameters::SelectionParameters()
{
    mainLayout_ = new QVBoxLayout();
    formLayout_ = new QFormLayout();
    formLayout_->setLabelAlignment(Qt::AlignLeft | Qt::AlignVCenter);

    setLayout(mainLayout_);

    mainLayout_->addLayout(formLayout_);

    formLayout_->addRow("Prim Path", new QLineEdit());

    primTypeParm = new QComboBox();
    primTypeParm->addItems({"Scope", "Mesh", "Xform", "Camera"});

    formLayout_->addRow("Prim Type", primTypeParm);
    formLayout_->addRow("Invert Winding Order", new QCheckBox());
    formLayout_->addRow("Animate", new QCheckBox());
}
