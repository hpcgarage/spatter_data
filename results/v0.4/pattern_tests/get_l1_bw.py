def get_bw_mbs(freq_ghz, bits_per_access, reads, writes, cores):
    freq_hz = freq_ghz * 1e9
    read_bits_per_sec  = freq_hz * reads  * bits_per_access * cores
    write_bits_per_sec = freq_hz * writes * bits_per_access * cores
    read_mbps  = read_bits_per_sec  / 8 / 1000 / 1000
    write_mbps = write_bits_per_sec / 8 / 1000 / 1000
    print("Read: {} MB/s".format(read_mbps))
    print("Write: {} MB/s".format(write_mbps))

print("Broadwell")
get_bw_mbs(2., 256, 2, 1, 10)
print("Cascade Lake")
get_bw_mbs(2., 512, 2, 1, 10)
print("Naples")
get_bw_mbs(2., 256, 2, 1, 10)
print("TX2")
get_bw_mbs(2., 128, 2, 1, 10)

