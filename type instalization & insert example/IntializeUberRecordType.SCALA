%spark
import org.insightedge.spark.implicits.all._
import org.insightedge.spark.context.InsightEdgeConfig
import model.v1._

sc.grid.getTypeManager().registerTypeDescriptor(classOf[UberRecord])
