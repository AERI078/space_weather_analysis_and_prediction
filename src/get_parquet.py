import pyarrow as pa
import pyarrow.parquet as pq
from space_weather_package import collect_data

gst_json = collect_data.collect_donki_data('GST')
gst_df = collect_data.get_dataframe('GST', gst_json)
gst_table = pa.Table.from_pandas(gst_df)
pq.write_table(gst_table, 'gst_data.parquet')


cme_json = collect_data.collect_donki_data('CME')
cme_df = collect_data.get_dataframe('CME', cme_json)
cme_table = pa.Table.from_pandas(cme_df)
pq.write_table(cme_table, 'cme_data.parquet')
