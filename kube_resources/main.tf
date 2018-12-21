provider "kubernetes" {
  host = "https://104.196.242.174"

  username = "ClusterMaster"
  password = "MindTheGap"
}

resource "kubernetes_deployment" "ghost" {
  
  spec {
    replicas = 2

    selector {
      match_labels {
        test = "ghost"
      }
    }

      spec {
        container {
          image = "ghost:latest"
          name  = "ghost"

          resources {
            limits {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests {
              cpu    = "250m"
              memory = "50Mi"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "ghost-load-balancer" {
  metadata {
    name = "ghost-load-balancer"
  }
  spec {
    selector {
      App = "${kubernetes_deployment.ghost.metadata.0.labels.App}"
    }
    port {
      port = 80
      target_port = 80
    }

    type = "LoadBalancer"
  }
}