<template>
  <div class="mb-5 text-start">
    <h2>Predictions and Confidence values</h2>
    <LineChart
      ref="lineChart"
      style="height: 300px"
      :chartData="chartData"
      :options="chartOptions"
      class="mb-2"
    />
    <div class="d-flex align-items-start">
      <button class="btn btn-secondary b-2" @click="resetZoom">
        Reset zoom
      </button>
    </div>
  </div>

  <div class="text-start">
    <h2>Data table of backup</h2>
    <ag-grid-vue
      ref="dataTable"
      style="width: 100%; height: 700px"
      class="ag-theme-alpine"
      :columnDefs="columnDefs"
      :rowData="rowData"
      rowSelection="multiple"
      :enableRangeSelection="true"
      pagination="true"
      paginationPageSize="30"
      @gridReady="onGridReady"
    >
    </ag-grid-vue>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { IBackupMetadata } from "@/store/Interfaces";
import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";
import { AgGridVue } from "ag-grid-vue3";
import { LineChart } from "vue-chart-3";
import { Chart, registerables } from "chart.js";
import zoomPlugin from "chartjs-plugin-zoom";

Chart.register(zoomPlugin);
Chart.register(...registerables);

export default defineComponent({
  name: "BackupList",
  props: {
    fileServerId: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      gridApi: null,
      chartOptions: {
        plugins: {
          zoom: {
            pan: {
              enabled: true,
              mode: "x",
              modifierKey: "ctrl",
            },
            zoom: {
              wheel: {
                enabled: true,
              },
              pinch: {
                enabled: true,
              },
              drag: {
                enabled: true,
              },
              mode: "x",
            },
          },
        },
      },
    };
  },
  components: {
    AgGridVue,
    LineChart,
  },
  beforeMount() {
    if (!this.getBackupMetadata) {
      this.fetchBackupMetadata();
    }
  },
  setup() {
    const lineChart = ref(null);
    const dataTable = ref(null);

    return {
      lineChart,
      dataTable,
    };
  },
  computed: {
    getBackupMetadata(): Array<IBackupMetadata> {
      return this.$store.getters.getBackupMetadata(this.fileServerId);
    },
    columnDefs() {
      let column = [
        {
          field: "date",
          resizable: true,
          sortable: true,
          filter: true,
        },
        {
          field: "MDM prediction",
          resizable: true,
          sortable: true,
          filter: true,
        },
        {
          field: "MDM confidence",
          resizable: true,
          sortable: true,
          filter: true,
        },
        {
          field: "OCSVM prediction",
          resizable: true,
          sortable: true,
          filter: true,
        },
        {
          field: "OCSVM confidence",
          resizable: true,
          sortable: true,
          filter: true,
        },
      ];
      if (this.getBackupMetadata) {
        let fields = this.getBackupMetadata[0].features;
        let toBeAddedFields = Object.keys(fields).map((data) => {
          return {
            field: data,
            resizable: true,
            sortable: true,
            filter: true,
          };
        });
        column = column.concat(toBeAddedFields);
        console.log(column);
      }
      return column;
    },
    rowData() {
      if (this.getBackupMetadata) {
        // eslint-disable-next-line vue/no-async-in-computed-properties
        setTimeout(() => this.resizeGridPane(), 500);
        return this.getBackupMetadata.map((backupdata) => {
          let c_pred = backupdata.predictions[0];
          let start_data = {
            date: new Date(backupdata.backup_date * 1000).toLocaleDateString(
              "en-US"
            ),
            "MDM prediction": c_pred["meta_data_model"]
              ? c_pred["meta_data_model"]["prediction"]
              : null,
            "MDM confidence": c_pred["meta_data_model"]
              ? Math.round(c_pred["meta_data_model"]["pred_confidence"] * 100) /
                100
              : null,
            "OCSVM prediction": c_pred["meta_data_model"]
              ? c_pred["meta_data_model"]["prediction"]
              : null,
            "OCSVM confidence": c_pred["meta_data_model"]
              ? Math.round(c_pred["meta_data_model"]["pred_confidence"] * 100) /
                100
              : null,
          };
          for (const [key, value] of Object.entries(backupdata.features)) {
            let val = Number(value);
            start_data[key] = Math.round(val * 100) / 100;
          }
          return start_data;
        });
      }
      return null;
    },

    chartData() {
      let charData;
      if (this.getBackupMetadata) {
        let labels = this.getBackupMetadata.map((backupdata) => {
          return new Date(backupdata.backup_date * 1000).toLocaleDateString(
            "en-US"
          );
        });

        let meta_dataprediction = this.getBackupMetadata.map((backupdata) => {
          let c_pred = backupdata.predictions[0];
          return c_pred["meta_data_model"]
            ? c_pred["meta_data_model"]["prediction"]
            : null;
        });
        let meta_pred_confidence = this.getBackupMetadata.map((backupdata) => {
          let c_pred = backupdata.predictions[0];
          return c_pred["meta_data_model"]
            ? c_pred["meta_data_model"]["pred_confidence"]
            : null;
        });

        let ocsvm_dataprediction = this.getBackupMetadata.map((backupdata) => {
          let c_pred = backupdata.predictions[0];
          return c_pred["path_ocsvm"]
            ? c_pred["path_ocsvm"]["prediction"]
            : null;
        });
        let ocsvm_pred_confidence = this.getBackupMetadata.map((backupdata) => {
          let c_pred = backupdata.predictions[0];
          return c_pred["path_ocsvm"]
            ? c_pred["path_ocsvm"]["pred_confidence"]
            : null;
        });

        return {
          labels: labels,
          datasets: [
            {
              label: "Meta Data Model Prediction",
              backgroundColor: "#f12d2d",
              data: meta_dataprediction,
            },
            {
              label: "Meta data confidence",
              backgroundColor: "#f68686",
              data: meta_pred_confidence,
            },
            {
              label: "Path OCSVM Prediction",
              backgroundColor: "#375cfd",
              data: ocsvm_dataprediction,
            },
            {
              label: "Path OCSVM confidence",
              backgroundColor: "#5e7cfc",
              data: ocsvm_pred_confidence,
            },
          ],
        };
      }
      return charData;
    },
  },
  methods: {
    resetZoom() {
      this.lineChart.chartInstance.resetZoom();
    },
    resizeGridPane() {
      this.columnApi.autoSizeAllColumns();
    },
    onGridReady(params) {
      this.gridApi = params.api;
      this.columnApi = params.columnApi;
      const sortModel = [{ colId: "date", sort: "asc" }];
      params.api.setSortModel(sortModel);
    },
    toDate(timeStamp: number) {
      return new Date(timeStamp * 1000).toDateString();
    },
    fetchBackupMetadata() {
      return this.$store.dispatch("getBackupMetadata", {
        fileServerId: this.fileServerId,
      });
    },
  },
});
</script>

<style lang="scss">
@import "~ag-grid-community/dist/styles/ag-grid.css";
@import "~ag-grid-community/dist/styles/ag-theme-balham.css";
</style>
