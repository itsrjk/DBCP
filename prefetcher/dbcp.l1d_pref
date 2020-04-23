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
uint64_t dbtable_hit;

// static std::map<uint64_t, uint64_t> CACHE::hist_table = std::map<uint64_t, uint64_t>();
using namespace std;

typedef map<uint64_t, uint64_t>::iterator history_iter;
typedef map<uint64_t, pair<uint8_t, uint64_t>>::iterator deadblock_iter;

uint64_t add_truncate(uint64_t, uint64_t, uint8_t);
uint64_t xor_encoding(uint64_t, uint64_t);
uint64_t cantor_encoding(uint64_t, uint64_t);
void insert_to_hist(uint64_t, uint64_t);
void print_hist_table();
void print_db_table();
uint64_t bitwise_add(uint64_t, uint64_t);
uint64_t bitwise_mul(uint64_t, uint64_t);
uint64_t bitwise_div(uint64_t, uint64_t);

// Define the class members
// hist_table - block_addr: [PC1, PC2, PC3...]
map<uint64_t, uint64_t> CACHE::hist_table;
// db_table - signature: [<2bit_saturating_counter, prefetch_addr>, ...]
map<uint64_t, pair<uint8_t, uint64_t>> CACHE::db_table;

void CACHE::l1d_prefetcher_initialize() 
{
    cout << "CPU " << cpu << " L1D DBCP prefetcher" << endl;
    cout << this->NAME << endl;
    dbtable_hit = 0;
}

void CACHE::l1d_prefetcher_operate(uint64_t addr, uint64_t ip, uint8_t cache_hit, uint8_t type)
{
    uint64_t tag = addr >> LOG2_BLOCK_SIZE;
    // update history table
    // insert_to_hist(tag, ip);

    if (!cache_hit) {
        uint64_t tag = addr >> LOG2_BLOCK_SIZE;
        // add new row to history table
        // this->hist_table[tag] = add_truncate(0, ip, 1);
        this->hist_table[tag] = ip;
    }
    else {
        // add this ip to the trace
        history_iter ht_itr = this->hist_table.find(tag);
        // if we found the element, i.e. iterator hasn't reached the end
        if (ht_itr != this->hist_table.end()) {
            // this->hist_table[tag] = add_truncate(this->hist_table[tag], ip, 0);
            this->hist_table[tag] = xor_encoding(this->hist_table[tag], ip);
        }
    }
    // if we are here and it was a cache miss, high probability that we skip the next block
    // b/c it's highly unlikely a block dies after a single access (goes against spatial locality assumptions)
    // this is the current trace for this block
    uint64_t signature = this->hist_table[tag];

    // Search if the current state of the trace for this block is in the deadblock table
    deadblock_iter db_itr = this->db_table.find(signature);
    if (db_itr != this->db_table.end()) {
        dbtable_hit++;
        // if found, this is a dead block, so increment the 2bit counter and prefetch
        uint8_t trace_count = this->db_table[signature].first;
        uint8_t pred_confidence = (trace_count >= ((MAX_COUNTER + 1)/2) ? 1 : 0);
        if (pred_confidence) {
            // if we are confident based on the counter, then invalidate this block
            invalidate_entry(tag);
            // and prefetch
            uint64_t pf_addr = this->db_table[signature].second;
            prefetch_line(ip, addr, pf_addr, FILL_L1, 0);
        }
    }
}

void CACHE::l1d_prefetcher_cache_fill(uint64_t addr, uint32_t set, uint32_t way, uint8_t prefetch, uint64_t evicted_addr, uint32_t metadata_in)
{
    // this will store the signature corresponding to the tag
    // of the block being evicted
    uint64_t signature;
    uint64_t tag_evict = evicted_addr >> LOG2_BLOCK_SIZE;
    history_iter ht_itr = this->hist_table.find(tag_evict);
    // found the signature in history table
    if (ht_itr != this->hist_table.end()) {
        signature = this->hist_table[tag_evict];

        // Note: the signature is our index into deadblock table

        // Move this block's trace from history table to deadblock table
        deadblock_iter db_itr = this->db_table.find(signature);
        if (db_itr == this->db_table.end()) {
            // if doesn't exist, add a new entry for this trace in deadblock table
            // initialise 2bit counter to 1, prefetch address = addr
            pair<uint8_t, uint64_t> new_trace (1, addr);
            this->db_table[signature] = new_trace;
        }
        else if ((this->db_table[signature].first < MAX_COUNTER)) {
            // if found, then just increment the counter,
            // i.e. another time this trace resulted in a dead block
            // each element in the table is a std::pair<> of counter, prefetch_addr
            this->db_table[signature].first += 1;
        }

        // Remove this block's entry from history table
        this->hist_table.erase(tag_evict);
    }
}

void CACHE::l1d_prefetcher_final_stats()
{
    cout << "CPU " << cpu << " L1D DBCP final stats" << endl;
    cout << "DBC Table size: " << this->db_table.size() << endl;
    cout << "DBC TABLE\tHIT:" << dbtable_hit << "\t" << endl;
    // cout << "DBC Table\n";
    // print_db_table();
}


//======== Helper Functions ========//
// xor used as encoding
uint64_t xor_encoding(uint64_t old_sig, uint64_t new_pc)
{
    return old_sig ^ new_pc;
}

// truncated addition: add and then truncate
uint64_t add_truncate(uint64_t old_sig, uint64_t new_pc, uint8_t first)
{
    // sanity check: upper limit on the number of bits
    // (we are not going above 30 in our experiments)
    if (BITS_TO_KEEP > 31) {
        return old_sig;
    }
    uint8_t BITS_TO_SHIFT = 64 - BITS_TO_KEEP;
    if (!first) {
        // bring the relevant bits back to LSP
        uint64_t old_sig = old_sig >> BITS_TO_SHIFT;
    }
    
    // add pc to the trace
    uint64_t signature = old_sig + new_pc;
    // keep only the last n bits
    signature = signature << BITS_TO_SHIFT;
    return signature;
}

// an implementation of cantor pairing which we use as one of the
// encoding algorithms
uint64_t cantor_encoding(uint64_t old_sig, uint64_t new_pc)
{
    uint64_t signature = bitwise_add(old_sig, new_pc);
    signature = bitwise_mul(signature, (signature+1));
    signature = bitwise_div(signature, 2);
    signature = bitwise_add(signature, new_pc);
    return signature;
}

// add new_pc to some element in the history table
// if tag doesn't exist, it will place new_pc there
// else, it will add new+pc to the existing trace encoding
void CACHE::insert_to_hist(uint64_t tag, uint64_t new_pc)
{
    history_iter itr = this->hist_table.find(tag);
    // if we found the element, i.e. iterator hasn't reached the end
    if (itr != this->hist_table.end()) {
        // this is not the first addr in trace, so pass 0 as last argument
        // this->hist_table[tag] = add_truncate(this->hist_table[tag], new_pc, 0);
        this->hist_table[tag] = xor_encoding(this->hist_table[tag], new_pc);
    }
    else {
        // this->hist_table[tag] = add_truncate(0, new_pc, 1);
        this->hist_table[tag] = new_pc;
    }
}

void CACHE::print_hist_table()
{
    for (auto i = this->hist_table.begin(); i != this->hist_table.end(); i++) {
        cout << "map: " << i->first << "\t" << i->second;
    }
    cout << endl;
}

void CACHE::print_db_table()
{
    for (auto i = this->db_table.begin(); i != this->db_table.end(); i++) {
        cout << i->first << ":\t" << i->second.first;
        cout << "::::" << i->second.second << endl;
    }
    cout << endl;
}

// Bitshifting for arithmetic operations
// using these since we are adding and multiplying large numbers
uint64_t bitwise_add(uint64_t a, uint64_t b)
{
    uint64_t carry  = a & b;
    uint64_t result = a ^ b;
    while(carry != 0)
    {
        // If you need the mathematical carry from addition,
        // check the overflow from this shift.
        uint64_t shiftedcarry = carry << 1;
        carry  = result & shiftedcarry;
        result = result ^ shiftedcarry;
    }
    return result;
}

uint64_t bitwise_mul(uint64_t a, uint64_t b)
{
    uint64_t result = 0;
    while(a != 0)
    {
        if(a & 1) // If the lowest order bit is set in A?
        {
            result = result + b;
        }
        a = a >> 1; // Note: This must set highest order bit ZERO. It must not copy the sign bit.
        b = b + b;  // Alternatively, left-shift by 1 bit
    }
    return result;
}

uint64_t bitwise_div(uint64_t dividend, uint64_t divisor)
{
    if(divisor == 0)
    {
        return 0;
    }
    uint64_t scaled_divisor = divisor;
    uint64_t remain         = dividend;
    uint64_t result   = 0;
    uint64_t multiple = 1;
        
    while(scaled_divisor < dividend)
    {
        scaled_divisor = scaled_divisor << 1; // Multiply by two.
        multiple       = multiple << 1;
    }
    do {
        if(remain >= scaled_divisor)
        {
            remain = remain - scaled_divisor;
            result = result + multiple;
        }
        scaled_divisor = scaled_divisor >> 1; // Divide by two.
        multiple       = multiple       >> 1;
    } while(multiple != 0);
    
    return result;
}