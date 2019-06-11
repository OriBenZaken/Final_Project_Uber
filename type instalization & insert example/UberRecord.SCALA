%define

package model.v1

import org.insightedge.scala.annotation._
import scala.beans.{BeanProperty, BooleanBeanProperty}

case class UberRecord(
    @BeanProperty
    @SpaceId(autoGenerate=true)
    var id: java.lang.String,

    @BeanProperty
    var latitude: java.lang.Double,

    @BeanProperty
    var longitude: java.lang.Double,

    @BeanProperty
    var base: java.lang.Integer,

    @BeanProperty
    var weekday : java.lang.Integer,

    @BeanProperty
    var day: java.lang.Integer,

    @BeanProperty
    var month: java.lang.Integer,

    @BeanProperty
    var year: java.lang.Integer,

    @BeanProperty
    var hour : java.lang.Integer,

    @BeanProperty
    var isWeekend: java.lang.Integer,

    @BeanProperty
    var isHoliday : java.lang.Integer,

    @BeanProperty
    var demand : java.lang.Integer
    ) {

  def this() = this(null,null,null,null,null,null,null,null,null,null,null,null)

}