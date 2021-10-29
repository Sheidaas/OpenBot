import ui
import playerm2g2
import chr
import textTail
import math
import dbg

class PlayerGauge(ui.Gauge):

	def __init__(self, parent):
		ui.Gauge.__init__(self)
		self.SetParent(parent)
		self.AddFlag("not_pick")
		self.MakeGauge(100, "red")

		self.curHP = 0
		self.maxHP = 0

		self.showAlways = False

	def __del__(self):
		ui.Gauge.__del__(self)

	def Hide(self):
		self.SetPosition(-100, -100)
		ui.Gauge.Hide(self)

	def OnUpdate(self):
		playerIndex = playerm2g2.GetMainCharacterIndex()

		(x, y, z)=textTail.GetPosition(playerIndex)

		isChat = textTail.IsChat(playerIndex)
		if math.isnan(x - self.GetWidth()/2) or math.isnan(y + 5):
			dbg.TraceError("playerIndex = %d, x = %f, y = %f, width = %f, isChat = %d" % (playerIndex, x, y, self.GetWidth(), isChat))
			return
		
		ui.Gauge.SetPosition(self, int(x - self.GetWidth()/2), int(y + 5) + isChat*17)

	def RefreshGauge(self):

		self.curHP = playerm2g2.GetStatus(playerm2g2.HP)
		self.maxHP = playerm2g2.GetStatus(playerm2g2.MAX_HP)
		self.SetPercentage(self.curHP, self.maxHP)

		if self.showAlways:
			self.Show()

		else:

			if self.IsShow():
				if self.curHP > self.maxHP / 2:
					self.Hide()

			else:
				if self.curHP < self.maxHP / 2:
					self.OnUpdate()
					self.Show()

	def EnableShowAlways(self):
		self.showAlways = True
		self.RefreshGauge()

	def DisableShowAlways(self):
		self.showAlways = False
		self.RefreshGauge()
