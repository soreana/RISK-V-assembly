#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


extern void my_assembly_function(void);

extern uint32_t result_L1;
extern uint32_t result_L2;

int main(void) {
  
  my_assembly_function();

  
  printf("L1 after 1 round: 0x%08x\n", result_L1);
  printf("L2 after 1 round: 0x%08x\n", result_L2);

  return 0;
}
