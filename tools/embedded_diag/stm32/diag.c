#include "diag.h"
#include <stdio.h>
#include <string.h>

// FreeRTOS headers - include only if present in the project
#ifdef FREERTOS_PRESENT
#include "FreeRTOS.h"
#include "task.h"
#endif

// Weak output hook. Implement this in your project to route messages to UART/LCD.
__attribute__((weak)) void diag_output(const char *msg) {
    // Default no-op implementation. Override in your project.
    (void)msg;
}

// --- Stub test implementations (replace with real checks) ---
static int sram_test(void) {
    // Implement a safe memory check if desired. Placeholder returns pass.
    return 1;
}

static int i2c_check_sensor(void) {
    // Try an I2C read from known address; return 1 on success, 0 on fail.
    return 1;
}

static int uart_loopback_test(void) {
    // If you have a UART loopback test, implement it. Placeholder returns pass.
    return 1;
}

static int sdcard_test(void) {
    // If an SD card and FATFS are available, perform a write/read test.
    return 1;
}

// Fill a JSON report into the provided buffer. Returns bytes written.
size_t diag_fill_report(char *buf, size_t buflen) {
    if (!buf || buflen < 128) return 0;
    int sram = sram_test();
    int i2c = i2c_check_sensor();
    int uart = uart_loopback_test();
    int sd = sdcard_test();

    int n = snprintf(buf, buflen,
        "{\n"
        "  \"sram_ok\": %d,\n"
        "  \"i2c_ok\": %d,\n"
        "  \"uart_ok\": %d,\n"
        "  \"sd_ok\": %d\n"
        "}\n",
        sram, i2c, uart, sd);

    if (n < 0) return 0;
    return (size_t)((n >= (int)buflen) ? (buflen - 1) : n);
}

#ifdef FREERTOS_PRESENT
static void DiagTask(void *pvParameters) {
    (void)pvParameters;
    char report[512];
    size_t len = diag_fill_report(report, sizeof(report));
    if (len > 0) {
        diag_output(report);
    } else {
        diag_output("{\"error\":\"failed to generate report\"}\n");
    }
    // Optionally run periodically; for now exit task after one run
    vTaskDelete(NULL);
}

static void IntroTask(void *pvParameters) {
    (void)pvParameters;
    // Simple placeholder intro: send a few frames via diag_output
    for (int i = 0; i < 6; ++i) {
        char msg[64];
        snprintf(msg, sizeof(msg), "Intro frame %d\n", i+1);
        diag_output(msg);
        vTaskDelay(pdMS_TO_TICKS(700));
    }
    vTaskDelete(NULL);
}

void diag_start_tasks(void) {
    // Create tasks with appropriate priorities and stack sizes. Adjust as needed.
    xTaskCreate(DiagTask, "Diag", 512, NULL, 3, NULL);
    xTaskCreate(IntroTask, "Intro", 256, NULL, 2, NULL);
}

#else
// If FreeRTOS is not present, provide a simple fallback that runs diagnostics inline.
void diag_start_tasks(void) {
    char report[512];
    diag_fill_report(report, sizeof(report));
    diag_output(report);
}
#endif
