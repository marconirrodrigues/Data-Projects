package com.marconirodrigues.cinema

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.text.TextUtils
import android.view.Gravity
import android.widget.GridLayout
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast

/** Grade com todos os apps. OK abre; segurar OK abre as informações do app. */
class AllAppsActivity : Activity() {

    private lateinit var grid: GridLayout

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_all_apps)
        grid = findViewById(R.id.grid)
    }

    override fun onResume() {
        super.onResume()
        populate()
    }

    private fun populate() {
        grid.removeAllViews()
        val density = resources.displayMetrics.density
        val usable = resources.displayMetrics.widthPixels - 2 * resources.getDimensionPixelSize(R.dimen.safe_h)
        val tileWidth = usable / grid.columnCount
        val iconSize = (56 * density).toInt()
        val margin = (6 * density).toInt()

        for (app in Apps.all(this)) {
            val tile = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                gravity = Gravity.CENTER_HORIZONTAL
                setPadding(margin * 2, margin * 2, margin * 2, margin * 2)
                setBackgroundResource(R.drawable.grid_tile_bg)
                isFocusable = true
                layoutParams = GridLayout.LayoutParams().apply {
                    width = tileWidth - 2 * margin
                    setMargins(margin, margin, margin, margin)
                }
                setOnFocusChangeListener { v, hasFocus ->
                    val s = if (hasFocus) 1.06f else 1f
                    v.animate().scaleX(s).scaleY(s).setDuration(120).start()
                }
                setOnClickListener { open(app) }
                setOnLongClickListener { showInfo(app); true }
            }
            tile.addView(ImageView(this).apply { setImageDrawable(app.icon) },
                LinearLayout.LayoutParams(iconSize, iconSize))
            tile.addView(TextView(this).apply {
                text = app.label
                setTextColor(getColor(R.color.text_dim))
                textSize = 13f
                gravity = Gravity.CENTER
                maxLines = 2
                ellipsize = TextUtils.TruncateAt.END
                setPadding(0, margin, 0, 0)
            })
            grid.addView(tile)
        }
        grid.getChildAt(0)?.requestFocus()
    }

    private fun open(app: Entry.App) {
        try {
            startActivity(app.intent)
        } catch (e: Exception) {
            Toast.makeText(this, getString(R.string.open_failed, app.label), Toast.LENGTH_SHORT).show()
        }
    }

    private fun showInfo(app: Entry.App) {
        runCatching {
            startActivity(Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:${app.pkg}")))
        }
    }
}
