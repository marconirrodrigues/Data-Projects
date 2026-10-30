package com.marconirodrigues.cinema

import android.animation.ArgbEvaluator
import android.animation.ValueAnimator
import android.app.Activity
import android.content.Intent
import android.graphics.Color
import android.graphics.Outline
import android.graphics.drawable.GradientDrawable
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Bundle
import android.view.KeyEvent
import android.view.View
import android.view.ViewOutlineProvider
import android.view.animation.DecelerateInterpolator
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import kotlin.math.abs

class HomeActivity : Activity() {

    private lateinit var dock: LinearLayout
    private lateinit var heroBanner: ImageView
    private lateinit var heroTitle: TextView
    private lateinit var heroSub: TextView
    private lateinit var hero: View
    private lateinit var wifi: ImageView
    private lateinit var wifiLabel: TextView

    private val glow = GradientDrawable().apply { gradientType = GradientDrawable.RADIAL_GRADIENT }
    private var glowColor = Color.rgb(94, 92, 230)
    private var glowAnimator: ValueAnimator? = null

    private var entries: List<Entry> = emptyList()
    private val items = ArrayList<View>()
    private var focused = 0
    private var signature = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)
        dock = findViewById(R.id.dock)
        hero = findViewById(R.id.hero)
        heroBanner = findViewById(R.id.heroBanner)
        heroTitle = findViewById(R.id.heroTitle)
        heroSub = findViewById(R.id.heroSub)
        wifi = findViewById(R.id.wifi)
        wifiLabel = findViewById(R.id.wifiLabel)

        val glowView = findViewById<View>(R.id.glow)
        glowView.background = glow
        glow.setGradientCenter(0.22f, 0.42f)
        glowView.addOnLayoutChangeListener { v, _, _, _, _, _, _, _, _ ->
            glow.gradientRadius = v.width * 0.75f
        }
        applyGlow(glowColor)
    }

    override fun onResume() {
        super.onResume()
        reloadIfChanged()
        updateNetwork()
        items.getOrNull(focused)?.requestFocus()
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        // Botão Home com o launcher já aberto: volta para o primeiro app
        items.firstOrNull()?.requestFocus()
    }

    @Deprecated("Tela inicial: o botão Voltar não tem para onde ir")
    override fun onBackPressed() = Unit

    override fun onKeyDown(keyCode: Int, event: KeyEvent): Boolean {
        if (keyCode == KeyEvent.KEYCODE_MENU) {
            startActivity(Intent(this, AllAppsActivity::class.java))
            return true
        }
        return super.onKeyDown(keyCode, event)
    }

    /** Recria o dock só quando apps foram instalados/removidos desde a última vez. */
    private fun reloadIfChanged() {
        val favorites = Apps.favorites(this)
        val shortcuts = Apps.shortcuts(this)
        val newSignature = (favorites.map { it.pkg } + shortcuts.map { it.label }).joinToString()
        if (newSignature == signature) return
        signature = newSignature
        entries = favorites + shortcuts
        buildDock(favorites.size)
        focused = focused.coerceIn(0, (items.size - 1).coerceAtLeast(0))
        entries.getOrNull(focused)?.let { showHero(it, animate = false) }
    }

    private fun buildDock(appCount: Int) {
        dock.removeAllViews()
        items.clear()
        val iconSize = resources.getDimensionPixelSize(R.dimen.dock_icon)
        val gap = resources.getDimensionPixelSize(R.dimen.dock_gap)
        val radius = resources.getDimension(R.dimen.tile_radius)

        entries.forEachIndexed { index, entry ->
            if (index == appCount && appCount > 0) dock.addView(divider(gap))

            val tile = FrameLayout(this).apply {
                layoutParams = LinearLayout.LayoutParams(iconSize, iconSize).apply {
                    marginStart = gap / 2; marginEnd = gap / 2
                }
                isFocusable = true
                contentDescription = entry.label
                outlineProvider = object : ViewOutlineProvider() {
                    override fun getOutline(view: View, outline: Outline) =
                        outline.setRoundRect(0, 0, view.width, view.height, radius)
                }
                clipToOutline = true
                if (entry is Entry.Shortcut) {
                    background = GradientDrawable().apply {
                        cornerRadius = radius
                        colors = intArrayOf(entry.accent, darken(entry.accent))
                        orientation = GradientDrawable.Orientation.TL_BR
                    }
                }
            }
            val image = ImageView(this).apply {
                setImageDrawable(entry.icon)
                scaleType = ImageView.ScaleType.FIT_CENTER
                if (entry is Entry.Shortcut) {
                    val pad = iconSize / 4
                    setPadding(pad, pad, pad, pad)
                }
            }
            tile.addView(image, FrameLayout.LayoutParams(iconSize, iconSize))
            tile.setOnFocusChangeListener { _, hasFocus ->
                if (hasFocus) onItemFocused(index)
            }
            tile.setOnClickListener { launch(entry) }
            dock.addView(tile)
            items += tile
        }
        // O foco não "escapa" pelas pontas do dock
        items.forEach { it.id = View.generateViewId() }
        items.firstOrNull()?.let { it.nextFocusLeftId = it.id }
        items.lastOrNull()?.let { it.nextFocusRightId = it.id }
    }

    private fun divider(gap: Int) = View(this).apply {
        layoutParams = LinearLayout.LayoutParams(dp(1), dp(40)).apply {
            marginStart = gap / 2; marginEnd = gap / 2
        }
        setBackgroundColor(getColor(R.color.glass_stroke))
    }

    /** Efeito "dock do macOS": o item em foco cresce e os vizinhos crescem um pouco. */
    private fun onItemFocused(index: Int) {
        val changed = index != focused
        focused = index
        val iconSize = resources.getDimensionPixelSize(R.dimen.dock_icon)
        items.forEachIndexed { i, view ->
            val scale = when (abs(i - index)) {
                0 -> 1.32f
                1 -> 1.12f
                else -> 1f
            }
            view.pivotY = view.height.toFloat()
            view.animate()
                .scaleX(scale).scaleY(scale)
                .translationY(-(scale - 1f) * iconSize * 0.15f)
                .translationZ(if (i == index) dp(8).toFloat() else 0f)
                .setDuration(180)
                .setInterpolator(DecelerateInterpolator())
                .start()
        }
        entries.getOrNull(index)?.let { showHero(it, animate = changed) }
    }

    private fun showHero(entry: Entry, animate: Boolean) {
        val banner = (entry as? Entry.App)?.banner
        heroBanner.setImageDrawable(banner)
        heroBanner.visibility = if (banner != null) View.VISIBLE else View.GONE
        heroTitle.visibility = if (banner != null) View.GONE else View.VISIBLE
        heroTitle.text = entry.label
        heroSub.text = entry.subtitle
        if (animate) {
            hero.alpha = 0f
            hero.translationX = dp(16).toFloat()
            hero.animate().alpha(1f).translationX(0f).setDuration(220)
                .setInterpolator(DecelerateInterpolator()).start()
        }
        animateGlow(entry.accent)
    }

    private fun animateGlow(target: Int) {
        glowAnimator?.cancel()
        glowAnimator = ValueAnimator.ofObject(ArgbEvaluator(), glowColor, target).apply {
            duration = 400
            addUpdateListener { applyGlow(it.animatedValue as Int) }
            start()
        }
    }

    private fun applyGlow(color: Int) {
        glowColor = color
        glow.colors = intArrayOf(withAlpha(color, 0x8C), withAlpha(color, 0x2E), Color.TRANSPARENT)
    }

    private fun launch(entry: Entry) {
        try {
            startActivity(entry.intent)
        } catch (e: Exception) {
            Toast.makeText(this, getString(R.string.open_failed, entry.label), Toast.LENGTH_SHORT).show()
        }
    }

    private fun updateNetwork() {
        val cm = getSystemService(ConnectivityManager::class.java)
        val caps = cm?.getNetworkCapabilities(cm.activeNetwork)
        val online = caps?.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET) == true
        wifi.alpha = if (online) 0.9f else 0.35f
        wifiLabel.visibility = if (online) View.GONE else View.VISIBLE
    }

    private fun dp(value: Int) = (value * resources.displayMetrics.density).toInt()

    private fun withAlpha(color: Int, alpha: Int) =
        Color.argb(alpha, Color.red(color), Color.green(color), Color.blue(color))

    private fun darken(color: Int): Int {
        val hsv = FloatArray(3)
        Color.colorToHSV(color, hsv)
        hsv[2] *= 0.7f
        return Color.HSVToColor(hsv)
    }
}
