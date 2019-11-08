# -*- coding: utf-8 -*-
"""novelWriter GUI Main Window StatusBar

 novelWriter – GUI Main Window StatusBar
=========================================
 Class holding the main window status bar

 File History:
 Created: 2019-04-20 [0.0.1]

"""

import logging
import nw

from time import time

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QColor, QPixmap, QFont
from PyQt5.QtWidgets import QStatusBar, QLabel, QFrame

logger = logging.getLogger(__name__)

class GuiMainStatus(QStatusBar):

    def __init__(self, theParent):
        QStatusBar.__init__(self, theParent)

        logger.debug("Initialising MainStatus ...")

        self.mainConf  = nw.CONFIG
        self.theParent = theParent
        self.refTime   = None

        self.iconGrey   = QPixmap(16,16)
        self.iconYellow = QPixmap(16,16)
        self.iconGreen  = QPixmap(16,16)

        self.monoFont = QFont("Monospace",10)

        self.iconGrey.fill(QColor(*self.theParent.theTheme.statNone))
        self.iconYellow.fill(QColor(*self.theParent.theTheme.statUnsaved))
        self.iconGreen.fill(QColor(*self.theParent.theTheme.statSaved))

        self.boxStats = QLabel()
        self.boxStats.setToolTip("Project Word Count | Session Word Count")

        self.boxTime = QLabel("")
        self.boxTime.setToolTip("Session Time")
        self.boxTime.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.boxTime.setFont(self.monoFont)

        self.boxCounts = QLabel()
        self.boxCounts.setToolTip("Document Character | Word | Paragraph Count")

        self.projChanged = QLabel("")
        self.projChanged.setFixedHeight(14)
        self.projChanged.setFixedWidth(14)
        self.projChanged.setToolTip("Project Changes Saved")

        self.docChanged = QLabel("")
        self.docChanged.setFixedHeight(14)
        self.docChanged.setFixedWidth(14)
        self.docChanged.setToolTip("Document Changes Saved")

        self.docLanguage = QLabel("")

        # Add Them
        self.addPermanentWidget(self.docChanged)
        self.addPermanentWidget(self.boxCounts)
        self.addPermanentWidget(QLabel("  "))
        self.addPermanentWidget(self.projChanged)
        self.addPermanentWidget(self.boxStats)
        self.addPermanentWidget(QLabel("  "))
        self.addPermanentWidget(self.boxTime)

        self.setSizeGripEnabled(True)

        self.sessionTimer = QTimer()
        self.sessionTimer.setInterval(1000)
        self.sessionTimer.timeout.connect(self._updateTime)
        self.sessionTimer.start()

        logger.debug("MainStatus initialisation complete")

        self.clearStatus()

        return

    def clearStatus(self):
        self.setRefTime(None)
        self.setStats(0,0)
        self.setCounts(0,0,0)
        self.setProjectStatus(None)
        self.setDocumentStatus(None)
        self._updateTime()
        return True

    def setRefTime(self, theTime):
        self.refTime = theTime
        return

    def setStatus(self, theMessage, timeOut=10.0):
        self.showMessage(theMessage, int(timeOut*1000))
        return

    def setProjectStatus(self, isChanged):
        if isChanged is None:
            self.projChanged.setPixmap(self.iconGrey)
        elif isChanged == True:
            self.projChanged.setPixmap(self.iconYellow)
        elif isChanged == False:
            self.projChanged.setPixmap(self.iconGreen)
        else:
            self.projChanged.setPixmap(self.iconGrey)
        return

    def setDocumentStatus(self, isChanged):
        if isChanged is None:
            self.docChanged.setPixmap(self.iconGrey)
        elif isChanged == True:
            self.docChanged.setPixmap(self.iconYellow)
        elif isChanged == False:
            self.docChanged.setPixmap(self.iconGreen)
        else:
            self.docChanged.setPixmap(self.iconGrey)
        return

    def setStats(self, pWC, sWC):
        self.boxStats.setText("<b>Project:</b> {:d} : {:d}".format(pWC,sWC))
        return

    def setCounts(self, cC, wC, pC):
        self.boxCounts.setText("<b>Document:</b> {:d} : {:d} : {:d}".format(cC,wC,pC))
        return

    ##
    #  Internal Functions
    ##

    def _updateTime(self):
        if self.refTime is None:
            theTime = "00:00:00"
        else:
            # This is much faster than using datetime format
            tS = int(time() - self.refTime)
            tM = int(tS/60)
            tH = int(tM/60)
            tM = tM - tH*60
            tS = tS - tM*60 - tH*3600
            theTime = "%02d:%02d:%02d" % (tH,tM,tS)
        self.boxTime.setText(theTime)
        return

# END Class GuiMainStatus
