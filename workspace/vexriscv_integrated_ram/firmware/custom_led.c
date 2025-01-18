// This file is Copyright (c) 2020 Florent Kermarrec <florent@enjoy-digital.fr>
// License: BSD

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <irq.h>
#include <libbase/uart.h>

int main(void)
{
#ifdef CONFIG_CPU_HAS_INTERRUPT
	irq_setmask(0);
	irq_setie(1);
#endif
	uart_init();

	uint32_t *ptr_leds = (volatile uint32_t *)CSR_LEDS_BASE;

	printf("Hello, Gabriel === I'm the VexRISCV!!!\n");
	while(1) {
		printf("OFF\n");
		*ptr_leds = 0;
		busy_wait(200);
		printf("ON\n");
		*ptr_leds = 1;
		busy_wait(200);
	}
	return 0;
}
