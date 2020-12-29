#include "addagenda.h"
#include "ui_addagenda.h"

AddAgenda::AddAgenda(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::AddAgenda)
{
    ui->setupUi(this);
}

AddAgenda::~AddAgenda()
{
    delete ui;
}
