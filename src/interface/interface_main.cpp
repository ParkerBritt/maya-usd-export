#include <QApplication>
#include <QLabel>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QLabel label("Hello, World!");
    label.setMinimumSize(200, 100);
    label.setAlignment(Qt::AlignCenter);
    label.show();

    return app.exec();
}
