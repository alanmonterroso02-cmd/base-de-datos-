#ifndef PIN_H
#define PIN_H
#include <Keypad.h>

const byte FILAS = 4;
const byte COLUMNAS = 4;

char teclas[FILAS][COLUMNAS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte pinesFilas[FILAS] = {13, 12, 14, 27};
byte pinesColumnas[COLUMNAS] = {26, 25, 33, 32};

Keypad teclado = Keypad(
                   makeKeymap(teclas),
                   pinesFilas,
                   pinesColumnas,
                   FILAS,
                   COLUMNAS
                 );

String pin = "";
bool capturandoPin = false;

void readpin(int longpin=0){
  

  char tecla = teclado.getKey();

  if (!tecla) return;

  // Entrar al modo PIN
  if (tecla == 'A' && !capturandoPin) {
    capturandoPin = true;
    pin = "";

    Serial.print("Ingrese PIN de ");
    Serial.print(longpin);
    Serial.println( " digitos");
    return;
  }

  // Capturar PIN
  if (capturandoPin) {

    if (tecla >= '0' && tecla <= '9') {

      pin += tecla;

      Serial.print("*"); // Oculta el PIN

      if (pin.length() == longpin) {

        Serial.println();
        Serial.print("PIN ingresado: ");
        Serial.println(pin);

        capturandoPin = false;

        // Aquí puedes enviar el PIN a la Raspberry Pi
        // Serial.println(pin);
      }
    }

    // Cancelar con *
    if (tecla == '*') {
      pin = "";
      capturandoPin = false;
      Serial.println("\nCancelado");
    }
  }
}
#endif
