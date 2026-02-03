#ifndef STM32_DIAG_H
#define STM32_DIAG_H

#include <stdint.h>
#include <stddef.h>

// Call to start background diagnostic task. Requires FreeRTOS to be running.
void diag_start_tasks(void);

// Fill a provided buffer with a JSON-formatted report. Buffer should be
// large enough (recommended >= 512 bytes). Returns number of bytes written.
size_t diag_fill_report(char *buf, size_t buflen);

// Weak hook: implement this in your platform to receive textual output
// (for example, send to UART or draw on an LCD). A default weak no-op is
// provided in diag.c so you must override it in your project.
void diag_output(const char *msg);

#endif // STM32_DIAG_H
