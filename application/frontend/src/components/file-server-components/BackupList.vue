<template>
  <div class="backup-list d-flex flex-wrap">
    <div
      class="card m-3"
      style="width: 18rem"
      v-for="backupMetadata in getBackupMetadata"
      :key="backupMetadata._id"
    >
      <div class="card-body">
        <div
          class="
            card-title
            d-flex
            justify-content-between
            align-items-baseline
            mb-4
          "
        >
          <h5>Backup</h5>
          <font-awesome-icon class="me-2" icon="database" />
        </div>
        <h6 class="card-subtitle mb-2 text-muted text-start">
          backed_up_amount: {{ backupMetadata.backed_up_amount }}
        </h6>
        <div class="card-text text-start">
          <div>
            <div class="text-muted">Data Range</div>
            <div class="ps-3">
              start: {{ toDate(backupMetadata.date_range.earliest_date) }}
            </div>
            <div class="ps-3">
              end: {{ toDate(backupMetadata.date_range.latest_date) }}
            </div>
          </div>
          <div>
            <div class="text-muted">File Actions</div>
            <div class="ps-3">
              Counts: {{ backupMetadata.uniques_counts.counts }}
            </div>
            <div class="ps-3">
              Uniques: {{ backupMetadata.uniques_counts.uniques }}
            </div>
          </div>
        </div>
        <div class="text-end hand-icon">
          <font-awesome-icon class="me-2" icon="hand-pointer" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { IBackupMetadata } from "@/store/Interfaces";

export default defineComponent({
  name: "BackupList",
  props: {
    fileServerId: {
      type: String,
      default: null,
    },
  },
  computed: {
    getBackupMetadata(): Array<IBackupMetadata> {
      return this.$store.getters.getBackupMetadata(this.fileServerId);
    },
  },
  mounted() {
    if (!this.getBackupMetadata) {
      this.fetchBackupMetadata();
    }
  },
  methods: {
    toDate(timeStamp: number) {
      return new Date(timeStamp * 1000).toDateString();
    },
    fetchBackupMetadata() {
      console.log("test1");
      return this.$store.dispatch("getBackupMetadata", {
        fileServerId: this.fileServerId,
      });
    },
  },
});
</script>
