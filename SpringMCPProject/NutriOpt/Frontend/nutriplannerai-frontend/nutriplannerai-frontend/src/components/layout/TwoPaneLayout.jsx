export default function TwoPaneLayout({ left, right }) {
  return (
    <main className="two-pane-layout">
      <section className="left-pane">{left}</section>
      <section className="right-pane">{right}</section>
    </main>
  );
}
