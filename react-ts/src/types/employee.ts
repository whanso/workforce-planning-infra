const Shifts = {
  MORNING: 'MORNING',
  AFTERNOON: 'AFTERNOON',
  EVENING: 'EVENING',
  NIGHT: 'NIGHT',
  WEEKEND: 'WEEKEND',
  WEEKDAY: 'WEEKDAY'
} as const;

export type Employee = {
  id: number,
  first: string,
  last: string,
  availableShifts: Array<typeof Shifts[keyof typeof Shifts]>,
  /**
   * List of timestamps for requested PTO
   */
  requestedPto: Array<string>
}