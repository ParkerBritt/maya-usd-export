#pragma once
#include <QtWidgets/QWidget>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QSpinBox>

class AnimationOptions : public QWidget
{
    Q_OBJECT
public:
    AnimationOptions();

    QFormLayout *m_formLayout;
    QCheckBox *doAnimationToggle;

    QSpinBox* m_animRangeStart;
    QSpinBox* m_animRangeEnd;
    QSpinBox* m_animRangeStep; 
    
private:
};
