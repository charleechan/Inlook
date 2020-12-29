#ifndef INLOOK_H
#define INLOOK_H

#include <QDialog>

namespace Ui {
class InLook;
}

class InLook : public QDialog
{
    Q_OBJECT

public:
    explicit InLook(QWidget *parent = nullptr);
    ~InLook();

private:
    Ui::InLook *ui;
};

#endif // INLOOK_H
