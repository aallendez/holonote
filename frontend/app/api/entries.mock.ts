import type { Entry } from "./entries";

function formatIso(date: Date) {
  return date.toISOString();
}

function randomInt(min: number, max: number) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

export function getMockEntries(count: number = 60): Entry[] {
  const now = new Date();
  const entries: Entry[] = [];

  // Seed with two examples similar to the provided backend shape
  const exampleDate = new Date();
  exampleDate.setDate(now.getDate() - 1);
  entries.push(
    {
      entry_id: "3d693d5f-7d55-46d0-92b2-d6d177be1353",
      user_id: "test-user",
      title: "Test Change",
      content: "I changed this entry",
      score: 8,
      entry_date: formatIso(exampleDate),
      created_at: formatIso(new Date(exampleDate.getTime() + 7 * 60 * 1000)),
      updated_at: formatIso(new Date(exampleDate.getTime() + 9 * 60 * 1000)),
      deleted_at: undefined,
    },
    {
      entry_id: "ea1aca8a-f3a4-4515-a90c-ab885d45bf12",
      user_id: "test-user",
      title: "Test",
      content: "Thiss is a test",
      score: 10,
      entry_date: formatIso(new Date(exampleDate.getTime() + 40 * 60 * 1000)),
      created_at: formatIso(new Date(exampleDate.getTime() + 40 * 60 * 1000)),
      updated_at: formatIso(new Date(exampleDate.getTime() + 40 * 60 * 1000)),
      deleted_at: undefined,
    },
  );

  // Generate additional entries scattered over the last ~30 weeks to fill the grid
  const daysBack = 30 * 7; // 30 weeks
  for (let i = 0; i < count; i++) {
    const dayOffset = randomInt(0, daysBack);
    const when = new Date(now);
    when.setHours(10, 0, 0, 0);
    when.setDate(now.getDate() - dayOffset);
    const id = cryptoRandomId();
    entries.push({
      entry_id: id,
      user_id: "test-user",
      title: `Entry #${i + 1}`,
      content: randomLorem(),
      score: skewedRandomScore(),
      entry_date: formatIso(when),
      created_at: formatIso(when),
      updated_at: formatIso(
        new Date(when.getTime() + randomInt(5, 90) * 60 * 1000),
      ),
      deleted_at: undefined,
    });
  }

  return entries;
}

function cryptoRandomId(): string {
  // Simple random UUID-ish string (not RFC compliant, but fine for mock)
  const s4 = () =>
    Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  return `${s4()}${s4()}-${s4()}-${s4()}-${s4()}-${s4()}${s4()}${s4()}`;
}

function randomLorem(): string {
  const samples = [
    "Reflected on today’s goals and next steps.",
    "Captured thoughts about a new idea.",
    "Summarized learnings from an article.",
    "Wrote about progress on the project.",
    "Daily check-in and gratitude notes.",
  ];
  return samples[randomInt(0, samples.length - 1)];
}

function skewedRandomScore(): number {
  const r = Math.random();
  return Math.max(1, Math.min(10, Math.round(10 - Math.pow(r, 2) * 9)));
}
