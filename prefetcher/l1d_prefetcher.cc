#include "cache.h"
#include "ooo_cpu.h"

void CACHE::l1d_prefetcher_initialize() 
{
    cout << "CPU " << cpu << " L1D DBCP prefetcher" << endl;
    cout << this->NAME << endl;

    for(uint32_t i=0;i<this->NUM_SET;i++){
        
        for (uint32_t j = 0; j < this->NUM_WAY; j++)
        {
            cout << this->block[i][j]->tag << endl;
        }
        

    }
}

void CACHE::l1d_prefetcher_operate(uint64_t addr, uint64_t ip, uint8_t cache_hit, uint8_t type)
{
    //uint64_t pf_addr = ((addr>>LOG2_BLOCK_SIZE)+1) << LOG2_BLOCK_SIZE;

    //DP ( if (warmup_complete[cpu]) {
    //cout << "[" << NAME << "] " << __func__ << hex << " base_cl: " << (addr>>LOG2_BLOCK_SIZE);
    //cout << " pf_cl: " << (pf_addr>>LOG2_BLOCK_SIZE) << " ip: " << ip << " cache_hit: " << +cache_hit << " type: " << +type << endl; });

    //prefetch_line(ip, addr, pf_addr, FILL_L1, 0);
}

void CACHE::l1d_prefetcher_cache_fill(uint64_t addr, uint32_t set, uint32_t way, uint8_t prefetch, uint64_t evicted_addr, uint32_t metadata_in)
{

}

void CACHE::l1d_prefetcher_final_stats()
{
    cout << "CPU " << cpu << " L1D DBCP final stats" << endl;
}
