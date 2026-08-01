/* Fund page: demo pledge + checkout */
(function () {
  const cfg = window.__FUND__ || { demoMode: true };
  const dialog = document.getElementById("pledge-dialog");
  const form = document.getElementById("pledge-form");
  const tierInput = document.getElementById("pledge-tier-id");
  const errEl = document.getElementById("pledge-error");
  const submitBtn = document.getElementById("pledge-submit");

  if (!dialog || !form) return;

  document.querySelectorAll("[data-pledge]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const tierId = btn.getAttribute("data-pledge");
      tierInput.value = tierId || "";
      if (errEl) {
        errEl.hidden = true;
        errEl.textContent = "";
      }
      if (typeof dialog.showModal === "function") {
        dialog.showModal();
      }
    });
  });

  form.addEventListener("submit", async function (ev) {
    const submitter = ev.submitter;
    if (submitter && submitter.value === "cancel") {
      return; // allow dialog close
    }
    if (submitter && submitter.value === "confirm") {
      ev.preventDefault();
      const tierId = tierInput.value;
      const displayName = document.getElementById("pledge-name").value.trim();
      const email = document.getElementById("pledge-email").value.trim();
      const publicName = document.getElementById("pledge-public").checked;

      if (errEl) {
        errEl.hidden = true;
        errEl.textContent = "";
      }
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Working…";
      }

      try {
        if (cfg.demoMode) {
          const res = await fetch("/api/fund/demo-pledge", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json" },
            body: JSON.stringify({
              tier_id: tierId,
              email: email || null,
              display_name: displayName || null,
              public: publicName,
            }),
          });
          const data = await res.json().catch(function () {
            return {};
          });
          if (!res.ok) {
            throw new Error(data.detail || data.message || "Pledge failed");
          }
          updateProgress(data.stats);
          prependLedgerRow(data.entry, displayName, publicName);
          dialog.close();
        } else {
          const res = await fetch("/api/fund/checkout", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json" },
            body: JSON.stringify({ tier_id: tierId, email: email || null }),
          });
          const data = await res.json().catch(function () {
            return {};
          });
          if (!res.ok) {
            throw new Error(data.detail || "Checkout failed");
          }
          if (data.mode === "demo" || !data.checkout_url) {
            // Fallback if server still in demo
            const res2 = await fetch("/api/fund/demo-pledge", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                tier_id: tierId,
                email: email || null,
                display_name: displayName || null,
                public: publicName,
              }),
            });
            const d2 = await res2.json();
            if (!res2.ok) throw new Error(d2.detail || "Pledge failed");
            updateProgress(d2.stats);
            prependLedgerRow(d2.entry, displayName, publicName);
            dialog.close();
          } else {
            window.location.href = data.checkout_url;
          }
        }
      } catch (err) {
        if (errEl) {
          errEl.hidden = false;
          errEl.textContent = err.message || String(err);
          errEl.style.color = "#f87171";
        }
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = "Confirm";
        }
      }
    }
  });

  function updateProgress(stats) {
    if (!stats) return;
    const raised = document.getElementById("raised-display");
    const count = document.getElementById("pledge-count");
    const fill = document.getElementById("progress-fill");
    const label = document.getElementById("progress-label");
    if (raised) {
      raised.textContent = "$" + (stats.raised_cents / 100).toFixed(2);
    }
    if (count) count.textContent = String(stats.pledge_count);
    if (fill) fill.style.width = (stats.progress_pct || 0) + "%";
    if (label) label.textContent = (stats.progress_pct || 0) + "% of goal";
  }

  function prependLedgerRow(entry, displayName, publicName) {
    if (!entry) return;
    const tbody = document.querySelector("#ledger-table tbody");
    if (!tbody) return;
    // Clear empty row
    const empty = tbody.querySelector("td[colspan]");
    if (empty) tbody.innerHTML = "";

    const tr = document.createElement("tr");
    const when = (entry.created_at || "").slice(0, 19) || "—";
    const name = publicName && displayName ? displayName : "Anonymous";
    const amount = "$" + (entry.amount_cents / 100).toFixed(2);
    tr.innerHTML =
      "<td class=\"small\">" +
      escapeHtml(when) +
      "</td><td>" +
      escapeHtml(name) +
      "</td><td>" +
      escapeHtml(entry.tier_name || "") +
      "</td><td>" +
      amount +
      "</td><td><span class=\"badge\">" +
      escapeHtml(entry.status || "demo") +
      "</span></td>";
    tbody.insertBefore(tr, tbody.firstChild);
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
})();
