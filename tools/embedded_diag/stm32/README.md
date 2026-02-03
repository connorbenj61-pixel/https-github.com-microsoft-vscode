# STM32 / FreeRTOS Self-Diagnostics Skeleton

This folder contains a minimal, portable skeleton you can drop into an STM32CubeIDE / CubeMX project to add a friendly "intro" animation and a background self-diagnostic task that reports results via a platform output function (for example, UART or LCD).

Files
- `diag.h` – Public interface to start the diagnostic task and to format a JSON report.
- `diag.c` – Implementation of a non-destructive diagnostics task and a weak `diag_output()` hook you should implement to route output to UART/LCD.
- `main_example.c` – Example integration showing how to start the intro and diag tasks and how to map `diag_output()` to `HAL_UART_Transmit`.

Design notes
- The diagnostics run as a FreeRTOS task (`DiagTask`) so they don't block the UI/intro animation.
- The built-in checks are intentionally conservative (non-destructive): SRAM basic check placeholder, UART loopback stub, I2C sensor read stub, SD card read/write stub.
- `diag_output(const char *)` is declared weak in `diag.c`. Provide your own implementation (for example, send to UART or write onto an LCD) in your project to receive JSON output.

Integration steps (CubeMX / STM32CubeIDE)
1. In CubeMX enable FreeRTOS and the peripherals you need (USART, I2C, SDIO/SPI for SD card, etc.).
2. Copy `diag.h`, `diag.c`, and `main_example.c` into your project `Src/` and `Inc/` folders.
3. In your project, implement `diag_output()` to forward strings to a UART or to draw them on-screen. Example in `main_example.c` shows mapping to `HAL_UART_Transmit`.
4. Build and flash. The example creates two tasks:
   - `IntroTask` (low priority) – plays a short intro animation (non-graphical placeholder included).
   - `DiagTask` (higher priority) – runs diagnostics and outputs a JSON summary.

Customizing tests
- Replace the stub functions (`sram_test()`, `i2c_check_sensor()`, etc.) with real hardware tests appropriate for your board.
- Keep tests non-destructive by default; provide an explicit destructive-test mode if needed.

Reporting
- The diagnostic JSON is printed via `diag_output()` once tests finish. You can store it on SD, or transmit over UART or network.

Security
- Do not expose private keys or credentials in diagnostic output.
- If you transmit reports over the network, use TLS and authenticated endpoints.

License
- Add your project's license when integrating these files.
