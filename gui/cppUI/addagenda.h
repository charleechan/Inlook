#ifndef ADDAGENDA_H
#define ADDAGENDA_H

#include <QWidget>

namespace Ui {
class AddAgenda;
}

class AddAgenda : public QWidget
{
    Q_OBJECT

public:
    explicit AddAgenda(QWidget *parent = nullptr);
    ~AddAgenda();

private:
    Ui::AddAgenda *ui;
};

#endif // ADDAGENDA_H
