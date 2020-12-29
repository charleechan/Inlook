#include "inlook.h"
#include "ui_inlook.h"

InLook::InLook(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::InLook)
{
    ui->setupUi(this);
}

InLook::~InLook()
{
    delete ui;
}
