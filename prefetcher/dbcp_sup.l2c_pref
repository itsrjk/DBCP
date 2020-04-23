/*
 * Implementation of Dead Block Correlating Prefetcher - Lai, Fide, Falsafi
 * Reuel Johm and Deepraj Pandey
 *
 * 28 April, 2020
 */

#include <map>
#include <utility> // for pair
#include "cache.h"
#include "ooo_cpu.h"

// for the 2-bit saturating counters corresponding to 
// the traces in deadblock table
#define MAX_COUNTER 3
#define BITS_TO_KEEP 30

using namespace std;

typedef map<uint64_t, uint64_t>::iterator history_iter;

uint64_t noncritical_misses;
void print_hist_table();


void CACHE::l2c_prefetcher_initialize() 
{
    cout << "CPU " << cpu << " L2C DBCP prefetcher" << endl;
    cout << this->NAME << endl;
    noncritical_misses = 0;
}

uint32_t CACHE::l2c_prefetcher_operate(uint64_t addr, uint64_t ip, uint8_t cache_hit, uint8_t type, uint32_t metadata_in)
{
    uint64_t tag = addr >> LOG2_BLOCK_SIZE;

    // if it hits in L2
    if (cache_hit) {
        // check if this missed in L1/is present in hist_table
        history_iter ht_itr = this->hist_table.find(tag);
        if (ht_itr != hist_table.end()) {
            // remove this non-critical miss
            this->hist_table.erase(tag);
            noncritical_misses++;
        }
    }
}

uint32_t CACHE::l2c_prefetcher_cache_fill(uint64_t addr, uint32_t set, uint32_t way, uint8_t prefetch, uint64_t evicted_addr, uint32_t metadata_in)
{

}

void CACHE::l2c_prefetcher_final_stats()
{
    cout << "CPU " << cpu << " L2C DBCP final stats" << endl;
    cout << "DBC Table size: " << this->db_table.size() << endl;
    cout << "NON-CRITICAL MISSES\tREMOVED:" << noncritical_misses << "\t" << endl;
    // cout << "DBC Table\n";
    // print_db_table();
}