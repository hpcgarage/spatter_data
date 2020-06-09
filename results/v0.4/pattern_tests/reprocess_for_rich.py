import pandas as pd

rename = {'pennant-006':'PENNANT-S0',
          'lulesh-000':'LULESH-S3',
          'lulesh-002':'LULESH-S1',
          'lulesh-003':'LULESH-S0',
          'lulesh-007':'LULESH-S2',
          'pennant-000' : 'PENNANT-G2',
          'pennant-001' : 'PENNANT-G3',
          'pennant-002' : 'PENNANT-G12',
          'pennant-003' : 'PENNANT-G0',
          'pennant-004' : 'PENNANT-G1',
          'pennant-005' : 'PENNANT-G7',
          'pennant-007' : 'PENNANT-G11',
          'pennant-008' : 'PENNANT-G9',
          'pennant-009' : 'PENNANT-G5',
          'pennant-010' : 'PENNANT-G15',
          'pennant-011' : 'PENNANT-G13',
          'pennant-012' : 'PENNANT-G14',
          'pennant-013' : 'PENNANT-G6',
          'pennant-014' : 'PENNANT-G8',
          'pennant-015' : 'PENNANT-G4',
          'pennant-016' : 'PENNANT-G10',
          'lulesh-001' : 'LULESH-G2',
          'lulesh-004' : 'LULESH-G3',
          'lulesh-005' : 'LULESH-G6',
          'lulesh-006' : 'LULESH-G4',
          'lulesh-008' : 'LULESH-G0',
          'lulesh-009' : 'LULESH-G7',
          'lulesh-010' : 'LULESH-G1',
          'lulesh-011' : 'LULESH-G5',
          'nekbone-000' : 'NEKBONE-G1',
          'nekbone-001' : 'NEKBONE-G0',
          'nekbone-002' : 'NEKBONE-G2',
          'amg-000' : 'AMG-G1',
          'amg-001' : 'AMG-G0',
          }

reindex = ['bdw', 'skx', 'clx', 'knl', 'npl', 'tx2', 'k40', 'titan', 'p100', 'gv100']


gather = pd.read_pickle("./radar_data_gather.pkl")
gather = gather.rename(columns=rename)
gather = gather.set_index('arch', drop=False)
gather = gather.reindex(reindex)

scatter = pd.read_pickle("./radar_data_scatter.pkl")
scatter = scatter.rename(columns=rename)
scatter = scatter.set_index('arch', drop=False)
scatter = scatter.reindex(reindex)

gather_abs = pd.read_pickle("./radar_data_gather_abs.pkl")
gather_abs = gather_abs.rename(columns=rename)
gather_abs = gather_abs.set_index('arch', drop=False)
gather_abs = gather_abs.reindex(reindex)

scatter_abs = pd.read_pickle("./radar_data_scatter_abs.pkl")
scatter_abs = scatter_abs.rename(columns=rename)
scatter_abs = scatter_abs.set_index('arch', drop=False)
scatter_abs = scatter_abs.reindex(reindex)

gather.to_pickle('pkl/app_gather_pct.pkl')
scatter.to_pickle('pkl/app_scatter_pct.pkl')
gather_abs.to_pickle('pkl/app_gather_abs.pkl')
scatter_abs.to_pickle('pkl/app_scatter_abs.pkl')
