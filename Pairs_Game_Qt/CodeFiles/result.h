#ifndef RESULT_H
#define RESULT_H

#include <QMainWindow>
#include "score.h"
#include <QMessageBox>
#include <QPushButton>
#include <QVBoxLayout>
#include <QLabel>

class Result : public QObject
{
    Q_OBJECT

public:
    Result(Score * score);
    Score * score;          // Score class to get current score.
    QPushButton * ng;       // New game button in the message box
    QPushButton * ex;       // Exit button in the message box

signals:
    void quit();            // Emitted when Quit button is clicked
    void newGame();         // Emitted when Restart button is clicked
    void freeze();          // Emitted at the beginning of the evaluation


public slots:
    void evaluate();        // Evaluate the endgame situation and prepares corresponig message box.


};

#endif // RESULT_H
