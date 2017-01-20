from maya.OpenMayaUI import MQtUtil


def _find_widget_ptr(widget):
    ptr = (MQtUtil.findControl(widget) or
           MQtUtil.findLayout(widget) or
           MQtUtil.findMenuItem(widget))
    return ptr


def _pyside2_as_qt_object(widget):
    from PySide2.QtCore import QObject
    from PySide2.QtWidgets import QWidget
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance
    ptr = _find_widget_ptr(widget)
    qobject = wrapInstance(long(ptr), QObject)
    meta = qobject.metaObject()
    _class = meta.className()
    _super = meta.superClass().className()
    qclass = getattr(QtWidgets, _class, getattr(QtWidgets, _super, QWidget))
    return wrapInstance(long(ptr), qclass)


def _pyside_as_qt_object(widget):
    from PySide.QtCore import QObject
    from PySide.QtGui import QWidget
    from PySide import QtGui
    from shiboken import wrapInstance
    ptr = _find_widget_ptr(widget)
    qobject = wrapInstance(long(ptr), QObject)
    meta = qobject.metaObject()
    _class = meta.className()
    _super = meta.superClass().className()
    qclass = getattr(QtGui, _class, getattr(QtGui, _super, QWidget))
    return wrapInstance(long(ptr), qclass)


def _pyqt4_as_qt_object(widget):
    from PyQt4.QtGui import QWidget
    from sip import wrapinstance
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    ptr = _find_widget_ptr(widget)
    return wrapinstance(long(ptr), QWidget)


def _pyqt5_as_qt_object(widget):
    from PyQt5.QtWidgets import QWidget
    from sip import wrapinstance
    ptr = _find_widget_ptr(widget)
    return wrapinstance(long(ptr), QWidget)

try:
    from PySide2 import QtCore, QtGui, QtWidgets
except ImportError:
    try:
        from PySide import QtCore, QtGui
        QtWidgets = QtGui
    except ImportError:
        try:
            from PyQt5 import QtCore, QtGui, QtWidgets
        except ImportError:
            try:
                from PyQt4 import QtCore, QtGui
                QtWidgets = QtGui
            except ImportError:
                pass
            else:
                as_qt_object = _pyqt4_as_qt_object
        else:
            as_qt_object = _pyqt5_as_qt_object
    else:
        as_qt_object = _pyside_as_qt_object
else:
    as_qt_object = _pyside2_as_qt_object

__all__ = ['QtCore', 'QtGui', 'as_qt_object']