#include "toast.h"
#include "ui_toast.h"

Toast::Toast(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Toast)
{
    ui->setupUi(this);
}

Toast::~Toast()
{
    delete ui;
}
