#include "interface/widgets/AnimationOptions.h"
#include "QtWidgets/qboxlayout.h"
#include "QtWidgets/qcheckbox.h"
#include <QtWidgets/QSpinBox>

AnimationOptions::AnimationOptions()
{
    m_formLayout = new QFormLayout();
    setLayout(m_formLayout);
    m_formLayout->setLabelAlignment(Qt::AlignLeft | Qt::AlignVCenter);

    doAnimationToggle = new QCheckBox();

    QHBoxLayout* animRangeLayout = new QHBoxLayout();
    m_animRangeStart = new QSpinBox();
    m_animRangeEnd = new QSpinBox();
    m_animRangeStep = new QSpinBox();
    m_animRangeStep->setValue(1);
    // set size policy
    m_animRangeStart->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
    m_animRangeEnd->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
    m_animRangeStep->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
    // set max min
    m_animRangeStart->setMaximum(99999);
    m_animRangeEnd->setMaximum(99999);
    m_animRangeStep->setMaximum(99999);
    // add to layout
    animRangeLayout->addWidget(m_animRangeStart, 3);
    animRangeLayout->addWidget(m_animRangeEnd, 3);
    animRangeLayout->addWidget(m_animRangeStep, 1);

    m_formLayout->addRow("Animation", doAnimationToggle);
    m_formLayout->addRow("Range", animRangeLayout);

    
}
