#ifndef TOAST_H
#define TOAST_H

#include <QWidget>

namespace Ui {
class Toast;
}

class Toast : public QWidget
{
    Q_OBJECT

public:
    explicit Toast(QWidget *parent = nullptr);
    ~Toast();

private:
    Ui::Toast *ui;
};

#endif // TOAST_H
